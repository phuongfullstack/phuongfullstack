<img src="assets/hero.svg" width="100%" alt="Phuong — full-stack developer. ASP.NET Core, Blazor, EF Core. Azure, Docker, GitHub Actions." />

I build web applications on **ASP.NET Core** — APIs and data access on the backend, Blazor or a JS framework on the frontend, containerised and shipped to Azure.

Most of my work sits in the Microsoft ecosystem, and most of my attention goes to the parts that are easy to get wrong: query performance, cache invalidation, and authorisation.

<img src="assets/stack.svg" width="100%" alt="Core: C#, .NET, ASP.NET Core, Blazor, EF Core. Toolbox: TypeScript, React, Angular, Vue, Azure, Docker, Kubernetes, GitHub Actions, SQL Server, PostgreSQL, Redis." />

```csharp
public sealed record Developer(string Name, string Role)
{
    public static Developer Me => new("Phuong", ".NET Full-Stack Developer");

    public string Philosophy => "Measure first. Cache second. Never trust user input.";
}
```

## What I work on

<details>
<summary><b>Backend</b> — ASP.NET Core, EF Core, API design</summary>

- **ASP.NET Core** (Web API & MVC) on modern .NET — minimal APIs, middleware, background services
- **EF Core** against SQL Server and PostgreSQL — migrations, compiled queries, split queries, killing N+1
- **API design** — versioning, FluentValidation, ProblemDetails, OpenAPI contracts clients can trust

</details>

<details>
<summary><b>Frontend</b> — Blazor, React, Angular, Vue</summary>

- **Blazor** Server & WebAssembly — component design, render modes, JS interop
- **React / Angular / Vue** wired to .NET APIs with typed clients generated from OpenAPI
- HTML5, CSS3, **TypeScript**, responsive layouts and accessible markup

</details>

<details>
<summary><b>Cloud &amp; DevOps</b> — Azure, Docker, CI/CD</summary>

- **Azure** — App Service, Functions, Container Apps, Key Vault, Application Insights
- **Docker** multi-stage builds — slim runtime images, health checks, sane layer caching
- **CI/CD** with GitHub Actions and Azure DevOps — build, test, scan, deploy on every push

</details>

<details>
<summary><b>Performance</b> — the part most people skip</summary>

- Query and **index tuning** driven by execution plans, not guesswork
- Fixing **N+1** and over-eager `Include` chains before they reach production
- **Caching** layers that actually invalidate — output caching, `IDistributedCache`, Redis
- Benchmarking with **BenchmarkDotNet**, so "faster" is a number rather than a feeling

</details>

<details>
<summary><b>Security</b> — secure by default</summary>

- **ASP.NET Core Identity**, JWT and cookie auth, policy-based authorisation
- Defence against **XSS, CSRF, SQL injection** and IDOR — parameterise everything, authorise every handler
- Secrets in **Key Vault**, never in `appsettings.json`

</details>

<details>
<summary><b>Testing</b> — so refactors aren't scary</summary>

- **xUnit / NUnit** with **Moq** or NSubstitute for unit tests
- Integration tests via **`WebApplicationFactory`** and **Testcontainers** against a real database
- Tests wired into CI — a red build blocks the merge

</details>

<!--
## Selected work

Điền 2–4 repo tiêu biểu vào đây rồi bỏ comment block này. Card tự render
tên repo, mô tả và ngôn ngữ — chỉ cần đổi `repo=`. Màu đã khớp sẵn với
hệ thiết kế trong assets/tokens.json.

Nếu chưa có gì để khoe thì cứ để nguyên trong comment: một section trống
còn tệ hơn là không có section.

<a href="https://github.com/phuongfullstack/REPO-NAME">
  <img src="https://github-readme-stats.vercel.app/api/pin/?username=phuongfullstack&repo=REPO-NAME&bg_color=0C0C10&title_color=A78BFA&text_color=9E9EB0&icon_color=A78BFA&border_color=26262F&border_radius=20" alt="REPO-NAME" />
</a>
<a href="https://github.com/phuongfullstack/OTHER-REPO">
  <img src="https://github-readme-stats.vercel.app/api/pin/?username=phuongfullstack&repo=OTHER-REPO&bg_color=0C0C10&title_color=A78BFA&text_color=9E9EB0&icon_color=A78BFA&border_color=26262F&border_radius=20" alt="OTHER-REPO" />
</a>
-->

## GitHub

<img src="https://github-readme-stats.vercel.app/api?username=phuongfullstack&show_icons=true&rank_icon=github&bg_color=0C0C10&title_color=A78BFA&text_color=9E9EB0&icon_color=A78BFA&border_color=26262F&border_radius=20" alt="GitHub stats for phuongfullstack" />
<img src="https://github-readme-stats.vercel.app/api/top-langs/?username=phuongfullstack&layout=compact&langs_count=8&bg_color=0C0C10&title_color=A78BFA&text_color=9E9EB0&icon_color=A78BFA&border_color=26262F&border_radius=20" alt="Most used languages by phuongfullstack" />

<img src="https://raw.githubusercontent.com/phuongfullstack/phuongfullstack/output/github-snake.svg" width="100%" alt="Snake eating the contribution graph of phuongfullstack" />

## Contact

Happy to talk about .NET architecture, a query that got slow, or a project you're planning.

<a href="https://linkedin.com/in/nhatphuongcse"><img src="https://img.shields.io/badge/LinkedIn-5B2BD9?style=flat-square&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
<a href="mailto:nhatphuongb1@gmail.com"><img src="https://img.shields.io/badge/Email-5B2BD9?style=flat-square&logo=gmail&logoColor=white" alt="Email" /></a>
<a href="https://github.com/phuongfullstack"><img src="https://img.shields.io/badge/GitHub-5B2BD9?style=flat-square&logo=github&logoColor=white" alt="GitHub" /></a>
