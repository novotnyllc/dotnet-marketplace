# Reactive Extensions (Rx.NET)

System.Reactive (Rx.NET) for composing asynchronous and event-based programs using observable sequences. Covers creating observables, key operators, error handling, scheduling, subscription lifecycle, bridging async/reactive, testing, and hot vs cold semantics.

Cross-references: `references/async-patterns.md` for async/await bridging, `references/channels.md` for Channel<T> as an alternative producer/consumer primitive.

---

## Package

```xml
<PackageReference Include="System.Reactive" Version="6.*" />
<PackageReference Include="Microsoft.Reactive.Testing" Version="6.*" /> <!-- for tests -->
```

---

## IObservable<T> / IObserver<T> Fundamentals

`IObservable<T>` is the push-based dual of `IEnumerable<T>`. `IObserver<T>` defines three callbacks: `OnNext(T)` delivers items, `OnError(Exception)` signals a terminal error, and `OnCompleted()` signals normal completion. Subscribing returns an `IDisposable` to cancel.

```csharp
IObservable<int> source = Observable.Range(1, 5);
IDisposable sub = source.Subscribe(
    onNext: x => Console.WriteLine(x),
    onError: ex => Console.WriteLine(ex.Message),
    onCompleted: () => Console.WriteLine("Done"));
sub.Dispose(); // Unsubscribe
```

---

## Creating Observables

```csharp
// Observable.Create -- most flexible factory
var src = Observable.Create<string>(obs => {
    obs.OnNext("Alpha"); obs.OnNext("Beta"); obs.OnCompleted();
    return Disposable.Empty;
});

// From events
var changes = Observable.FromEventPattern<FileSystemEventArgs>(watcher, nameof(watcher.Changed))
    .Select(ep => ep.EventArgs);

// Timer / Interval
var delayed = Observable.Timer(TimeSpan.FromSeconds(2));     // Emits 0L after 2s
var ticks   = Observable.Interval(TimeSpan.FromMilliseconds(500)); // 0L, 1L, 2L... every 500ms

// From async
var response = Observable.FromAsync(ct => httpClient.GetAsync("/data", ct));

// Subject<T> -- both IObservable and IObserver; use sparingly
var subject = new Subject<int>();
subject.Subscribe(x => Console.WriteLine(x));
subject.OnNext(1);
subject.OnCompleted();
```

---

## Key Operators

```csharp
// Filtering and transformation
source.Where(x => x > 10).Select(x => x * 2).DistinctUntilChanged();

// SelectMany -- project each element to an observable, flatten results
customerIds.SelectMany(id => GetOrdersForCustomer(id));

// Aggregation
source.Scan(0, (acc, x) => acc + x);      // Running total (emits each step)
source.Aggregate(0, (acc, x) => acc + x);  // Final total (emits once on completion)
```

### Combining Sequences

| Operator | Behavior |
|----------|----------|
| `Merge` | Interleaves items from multiple sources as they arrive |
| `CombineLatest` | Emits when any source emits, pairing with latest from others |
| `Zip` | Pairs items 1:1; waits for both sources to have an item |
| `Concat` | Subscribes to next source only after previous completes |

### Buffering, Windowing, Rate Limiting

```csharp
source.Buffer(5);                               // Collect into lists of 5
source.Buffer(TimeSpan.FromSeconds(1));          // Collect by time window
source.Window(TimeSpan.FromSeconds(1))           // Sub-observables per window
    .SelectMany(w => w.Count());

// Throttle = debounce (emits after quiet period). Sample = emit latest at fixed interval.
searchText.Throttle(TimeSpan.FromMilliseconds(300))
    .DistinctUntilChanged()
    .SelectMany(q => Observable.FromAsync(ct => searchApi.SearchAsync(q, ct))
        .Catch<SearchResult, Exception>(_ => Observable.Empty<SearchResult>()))
    .ObserveOn(SynchronizationContext.Current)
    .Subscribe(r => DisplayResults(r));
```

---

## Error Handling

```csharp
source.Catch<int, TimeoutException>(ex => Observable.Return(-1)); // Fallback on specific error
source.Retry(3);                                                   // Resubscribe up to 3 times
source.OnErrorResumeNext(fallbackSource);                          // Continue regardless of error
```

`Retry` resubscribes from scratch -- for cold observables this re-executes the entire source.

---

## Scheduling

| Operator | Controls |
|----------|----------|
| `SubscribeOn(scheduler)` | Where the subscription (production) logic runs |
| `ObserveOn(scheduler)` | Where the observer callbacks run |

| Scheduler | Use case |
|-----------|----------|
| `TaskPoolScheduler.Default` | Background work via thread pool |
| `CurrentThreadScheduler.Instance` | Trampoline on current thread |
| `ImmediateScheduler.Instance` | Synchronous inline -- useful for testing |
| `EventLoopScheduler` | Dedicated single-thread event loop |

```csharp
source.SubscribeOn(TaskPoolScheduler.Default)
    .ObserveOn(SynchronizationContext.Current)  // UI thread
    .Subscribe(x => UpdateUI(x));
```

---

## Subscription Management

```csharp
// CompositeDisposable -- bulk disposal of multiple subscriptions
var disposables = new CompositeDisposable();
disposables.Add(source1.Subscribe(x => HandleA(x)));
disposables.Add(source2.Subscribe(x => HandleB(x)));
disposables.Dispose(); // Disposes all

// SerialDisposable -- auto-disposes previous when replaced (cancel-and-restart)
var serial = new SerialDisposable();
serial.Disposable = source.Subscribe(x => Handle(x)); // Previous sub auto-disposed
```

---

## Bridging Async and Reactive

```csharp
// Task -> Observable (cold -- executes on each subscription)
var obs = Observable.FromAsync(ct => GetDataAsync(ct));

// Observable -> Task
int first = await source.FirstAsync();
int last  = await source.LastAsync();
```

---

## Hot vs Cold Observables

| Aspect | Cold | Hot |
|--------|------|-----|
| Production | Starts on subscribe | Producing regardless of subscribers |
| Sharing | Each subscriber gets own sequence | All subscribers share the stream |
| Examples | `Observable.Create`, `FromAsync` | `Subject<T>`, mouse events, stock feeds |
| Late subscriber | Gets all items from start | Misses items emitted before subscribing |

```csharp
// Share a cold observable with multiple observers
var shared = coldSource.Publish().RefCount(); // Auto-connect on first sub, disconnect on last
```

---

## When to Use Rx vs Alternatives

| Scenario | Recommended |
|----------|-------------|
| Complex event composition (merge, throttle, window) | **Rx** |
| Simple producer/consumer pipeline | **Channel<T>** |
| Async iteration over finite data | **IAsyncEnumerable<T>** |
| One-shot async operation | **Task<T>** |
| Standard event subscription without composition | **Plain events** |

---

## Testing with TestScheduler

```csharp
[Fact]
public void Throttle_EmitsAfterQuietPeriod()
{
    var scheduler = new TestScheduler();
    var source = scheduler.CreateHotObservable(
        ReactiveTest.OnNext(100, "a"),
        ReactiveTest.OnNext(200, "b"),
        ReactiveTest.OnNext(600, "c"),
        ReactiveTest.OnCompleted<string>(700));

    var results = scheduler.CreateObserver<string>();
    source.Throttle(TimeSpan.FromTicks(300), scheduler).Subscribe(results);
    scheduler.Start();

    results.Messages.AssertEqual(
        ReactiveTest.OnNext(500, "b"),
        ReactiveTest.OnNext(700, "c"),
        ReactiveTest.OnCompleted<string>(700));
}
```

Always inject `IScheduler` into production code to allow `TestScheduler` substitution in tests.

---

## R3 (Modern Alternative)

[R3](https://github.com/Cysharp/R3) by Cysharp is a ground-up reimplementation with zero-allocation operators, struct-based observers, and built-in frame scheduling for Unity. Not a drop-in replacement. Use R3 for new projects needing max throughput or Unity; use System.Reactive for the mature ecosystem and existing codebases.

---

## Agent Gotchas

1. **Do not forget to dispose subscriptions.** Every `Subscribe` returns `IDisposable`. Undisposed subscriptions leak memory. Use `CompositeDisposable` to manage lifetime.
2. **Do not confuse `Throttle` with `Sample`.** `Throttle` is a debounce (waits for quiet period). `Sample` emits the latest at fixed intervals. Agents frequently swap these.
3. **Do not ignore hot vs cold semantics.** Subscribing twice to a cold observable executes the side effect twice (e.g., two HTTP requests). Use `Publish().RefCount()` to share.
4. **Do not use `Subject<T>` as an event bus.** Subjects break declarative composition. Prefer `Observable.Create` or event bridging.
5. **Do not use default schedulers in UI code.** Without `ObserveOn(SynchronizationContext.Current)`, callbacks run on thread pool threads, causing cross-thread exceptions.
6. **Do not test time-dependent pipelines without `TestScheduler`.** Wall-clock tests are flaky. Inject `IScheduler` and use `TestScheduler`.
7. **Do not use unbounded `Retry()`.** It creates an infinite resubscription loop on failing cold observables. Always specify a max count.

---

## References

- [Rx.NET GitHub](https://github.com/dotnet/reactive)
- [IObservable<T> API](https://learn.microsoft.com/en-us/dotnet/api/system.iobservable-1)
- [System.Reactive on NuGet](https://www.nuget.org/packages/System.Reactive)
- [R3 by Cysharp](https://github.com/Cysharp/R3)
