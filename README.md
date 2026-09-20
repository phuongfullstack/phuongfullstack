<img src="assets/hero.svg" width="100%" alt="Phuong — senior full-stack developer. .NET, Angular, EF Core. Azure, Terraform, GitHub Actions." />

Eight years building production web and desktop systems — **.NET** on the backend, **Angular** (or whichever framework the product already has) on the frontend, provisioned with **Terraform** and shipped to **Azure**.

Most of my work sits in the Microsoft ecosystem, and I increasingly own systems end to end: infrastructure and architecture through backend, frontend and DevOps. Most of my attention goes to the parts that are easy to get wrong — query performance, cache invalidation, and authorisation.

**Right now:** architect engineer on an AI-driven enterprise procurement platform, team of ten. Azure infrastructure as code, .NET services, an Angular front end, OAuth2/OIDC at every service boundary, and observability wired in from the start across four isolated environments.

<img src="assets/numbers.svg" width="100%" alt="By the numbers: 113 months of .NET in production, 16 projects delivered end to end, 10 domains from fintech through gaming, 12 people in the largest team worked in." />

## What I work with

<img src="assets/stack.svg" width="100%" alt="Core: C#, .NET, ASP.NET Web API, EF Core, Angular. Toolbox: TypeScript, Vue 3, Svelte, React, Next.js, Azure, AWS, Docker, Terraform, GitHub Actions, SQL Server, PostgreSQL, MongoDB, Redis, RabbitMQ, Auth0, Serilog, Playwright, k6, WPF." />

<img src="assets/depth.svg" width="100%" alt="Months of project time per technology: .NET / C# 113, TypeScript 68, Angular 65, Entity Framework 55, Azure 52, SQL Server 49, GitHub Actions 34, Terraform 26." />

## How I build it

<img src="assets/architecture.svg" width="100%" alt="Request path from an Angular SPA through an ASP.NET Web API to EF Core and SQL Server or Postgres, with Redis alongside for caching and queues. Delivery: GitHub Actions builds, tests and scans, Terraform provisions four environments, and the result runs on Azure." />

```csharp
public sealed record Developer(string Name, string Role)
{
    public static Developer Me => new("Phuong", "Senior Full-Stack Developer");

    public int      Years      => 8;
    public string   Now        => "Architect Engineer — procurement platform, team of 10";
    public string[] Domains    => ["Healthcare", "Fintech", "Procurement SaaS",
                                   "Public Sector", "Education", "Gaming"];

    public string Philosophy => "Measure first. Cache second. Never trust user input.";
}
```

## What I work on

<details>
<summary><b>Backend</b> — ASP.NET Web API, EF Core, API design</summary>

- **ASP.NET Web API** on modern .NET — layered architecture, dependency injection, background workers
- **EF Core** against SQL Server and PostgreSQL — migrations, query tuning, killing N+1
- **Integration** — bidirectional REST contracts, event-based publish/subscribe, SignalR and raw
  WebSockets where a UI needs live state, gRPC, and services behind a Kong API gateway

</details>

<details>
<summary><b>Frontend</b> — Angular, Vue, React, Svelte</summary>

- **Angular** is where most of the hours are — SPAs with shared base component libraries
  (tables, forms, charts) built to speed the rest of the team up
- **Vue 3, Svelte, Ember, Next.js and plain JavaScript** where a product already had one
- HTML5, CSS3, **TypeScript**, Material, Bootstrap and Kendo UI; responsive, accessible markup

</details>

<details>
<summary><b>Cloud &amp; DevOps</b> — Azure, Docker, CI/CD</summary>

- **Azure** — App Service, Functions, Service Bus, Application Insights; **AWS** — S3, SQS, SNS,
  CloudFront, Elastic Beanstalk
- **Terraform** (and Bicep) — infrastructure as code, four identical environments so a release is
  promoted rather than rebuilt
- **Docker** multi-stage builds — slim runtime images, sane layer caching
- **CI/CD** with GitHub Actions and Azure DevOps — multi-stage pipelines with quality gates

</details>

<details>
<summary><b>Observability &amp; performance</b> — the part most people skip</summary>

- **Structured logging** with Serilog, distributed tracing and metrics — wired in from the start,
  not after the first SLA breach, and held against SLA / RTO / RPO targets
- **Azure Application Insights** and Azure Monitor across service endpoints
- Query and **index tuning** driven by execution plans, not guesswork; fixing **N+1** before production
- **Caching and queues** on Redis, with asynchronous workers for the slow work
- **k6** for load and performance, so "faster" is a number rather than a feeling

</details>

<details>
<summary><b>Security</b> — secure by default</summary>

- **OAuth2 / OIDC via Auth0**, applied at every service boundary, with token handling across services
- Defence against **XSS, CSRF, SQL injection** and IDOR — parameterise everything, authorise every handler
- Secrets kept out of `appsettings.json` and out of the repository

</details>

<details>
<summary><b>Architecture &amp; team</b></summary>

- **Clean / layered / hexagonal** architecture and **DDD**; microservices, serverless, containerised
  workloads; dependency injection and NuGet versioning across a shared codebase
- Set coding standards and bootstrap codebases other engineers build on
- Code review and mentoring on every team — lead on a team of four, architect on a team of ten
- **AI-assisted development** with Copilot, Cursor and Claude
- English: upper intermediate (B2)

</details>

<details>
<summary><b>Testing</b> — so refactors aren't scary</summary>

- **xUnit / NUnit** with **Moq** for unit tests; **Jest** and **Jasmine** on the front end
- **Playwright** end-to-end on the flows that must not break, **k6** for load
- **Codacy** and **Codecov** gates — a red build blocks the merge

</details>

## What I've built

Client and product work under NDA, so this is the shape of it rather than a list of names.

| Domain | When | Time | Built with |
| --- | --- | --- | --- |
| **Enterprise procurement SaaS** | 2025 – now | 16 mo | `.NET` `Angular` `Next.js` `Azure` `Terraform` `Auth0` |
| Consumer subscription apps | 2024 – 2025 | 18 mo | `Java` `Ember` `AWS` `Stripe` |
| Fintech &amp; fund management | 2024 | 10 mo | `.NET` `Angular` `SQL Server` `Terraform` |
| Gaming systems | 2024 – 2025 | 3 mo | `.NET Core` `VanillaJS` `WebSocket` `Docker` |
| AI &amp; PropTech | 2025 | 5 mo | `.NET Core` `Vue 3` `Postgres` `Redis` |
| Healthcare | 2023 – 2024 | 13 mo | `.NET` `Angular` `Azure Serverless` |
| Public sector | 2022 – 2023 | 13 mo | `.NET` `ASP.NET Web API` `SQL Server` `Serilog` |
| Data platforms &amp; ETL | 2022 – 2023 | 15 mo | `.NET` `OrientDB` `Svelte` `WPF` |
| Education &amp; enterprise web | 2019 – 2021 | 30 mo | `.NET` `Angular` `SQL Server` `VB.NET` |
| Blockchain | 2018 – 2019 | 11 mo | `Solidity` `React` `Ethereum` |

A few of them, concretely:

- **Procurement platform** — architected the Azure infrastructure in Terraform, bootstrapped the
  codebase, and set the layered design and coding standards a team of ten builds on. Integration
  contracts are bidirectional REST plus event-based publish/subscribe; every service boundary is
  behind OAuth2/OIDC. Four isolated environments, so a release is promoted rather than rebuilt.
- **Consumer photo-sharing app** — Java APIs and an Ember web app for a platform with millions of
  users, with Stripe, Apple In-App Purchase, Google Play Billing and TaxJar all resolving to one
  subscription state.
- **Gaming kiosk module** — re-architected a legacy terminal module onto modern .NET, mapped the
  existing hardware protocols, and drove the touchscreen over a WebSocket so the screen never polls.
- **Legacy system modelling** — sole developer on a tool that ETLs a codebase into a graph model and
  draws it, so analysts can see an undocumented architecture before planning a migration.

## Experience

| Years | Setting | Role |
| --- | --- | --- |
| **2025 – now** | Enterprise procurement platform | Architect Engineer — full-stack &amp; DevOps |
| **2024 – 2025** | Product delivery partner | Full-stack Developer, lead on one build |
| **2022 – 2024** | Enterprise software services | Full-stack Developer, code review &amp; mentoring |
| **2021 – 2022** | Offshore product engineering | Full-stack Developer |
| **2019 – 2021** | Software outsourcing studio | Full-stack Developer |
| **2018 – 2019** | Blockchain startup | Scrum Master &amp; Frontend |

🎓 **Duy Tan University** — B.Eng. Software Engineering &nbsp;·&nbsp; 🗣 English: upper intermediate (B2)

## GitHub

<img src="https://raw.githubusercontent.com/phuongfullstack/phuongfullstack/output/github-snake.svg?v=2" width="100%" alt="Snake eating the contribution graph." />

<sub>Every card above is generated by <a href="https://github.com/phuongfullstack/phuongfullstack/actions/workflows/profile-assets.yml">a workflow in this repository</a> — no third-party stats service.</sub>

## Contact

Happy to talk about .NET architecture, infrastructure as code, a query that got slow, or a project you're planning.

Full project history and seven architecture write-ups on the portfolio: **[phuongfullstack.github.io](https://phuongfullstack.github.io)**

<a href="https://linkedin.com/in/nhatphuongcse"><img src="https://img.shields.io/badge/LinkedIn-5B2BD9?style=flat-square&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
<a href="mailto:nhatphuongb1@gmail.com"><img src="https://img.shields.io/badge/Email-5B2BD9?style=flat-square&logo=gmail&logoColor=white" alt="Email" /></a>
<a href="https://github.com/phuongfullstack"><img src="https://img.shields.io/badge/GitHub-5B2BD9?style=flat-square&logo=github&logoColor=white" alt="GitHub" /></a>
