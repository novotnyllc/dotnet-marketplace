# fn-5-architecture-patterns-skills.5 Container skills

## Description
Create two container skills: `dotnet-containers` (multi-stage Dockerfiles, `dotnet publish` container images for .NET 8+, rootless containers, health checks) and `dotnet-container-deployment` (deploying .NET containers with Kubernetes Deployment + Service + probe YAML, Docker Compose for local dev, CI/CD integration).

## Acceptance
- [ ] `skills/architecture/dotnet-containers/SKILL.md` exists with `name` and `description` frontmatter
- [ ] `skills/architecture/dotnet-container-deployment/SKILL.md` exists with `name` and `description` frontmatter
- [ ] `dotnet-containers` covers multi-stage Dockerfiles, dotnet publish images, rootless containers, health checks
- [ ] `dotnet-container-deployment` includes Kubernetes Deployment + Service + probe YAML guidance
- [ ] `dotnet-container-deployment` covers Docker Compose for local dev and CI/CD integration
- [ ] `dotnet-container-deployment` cross-references `[skill:dotnet-observability]` for health check patterns
- [ ] `dotnet-container-deployment` states advanced CI patterns → fn-19 (out-of-scope)
- [ ] Skill `name` values are unique repo-wide
- [ ] Does NOT modify `plugin.json` (handled by fn-5.6)

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
