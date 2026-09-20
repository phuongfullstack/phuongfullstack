<div align="center">
  <img src="assets/header.svg" width="100%" alt="Phuong — .NET Full-Stack Developer" />
</div>

<div align="center">
  <img src="assets/typing.svg" alt="ASP.NET Core / Blazor / EF Core — Azure / Docker / GitHub Actions — Measure first. Cache second." />
</div>

<div align="center">
  <a href="https://linkedin.com/in/phuongfullstack"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
  <a href="mailto:contact@phuongfullstack.com"><img src="https://img.shields.io/badge/Email-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" /></a>
  <a href="https://phuongfullstack.com"><img src="https://img.shields.io/badge/Website-000000?style=for-the-badge&logo=aboutdotme&logoColor=white" alt="Website" /></a>
</div>

<br />

```csharp
public sealed record Developer(string Name, string Role)
{
    public static Developer Me => new("Phuong", ".NET Full-Stack Developer");

    public IReadOnlyList<string> Focus =>
    [
        "ASP.NET Core APIs that stay fast as the data grows",
        "Blazor & TypeScript front-ends that don't fight the backend",
        "Azure deployments you can redeploy on a Friday"
    ];

    public string Philosophy => "Measure first. Cache second. Never trust user input.";
}
```

<br />

<div align="center">

### 🧰 Tech Stack

<img src="assets/tech-stack.svg" alt="C#, .NET, Blazor, TypeScript, React, Angular, Vue, Azure, Docker, Kubernetes, GitHub Actions, SQL Server, PostgreSQL, Redis" />

</div>

---

## 🔍 What I work on

<details open>
<summary><b>⚙️ Backend &nbsp;—&nbsp; ASP.NET Core, EF Core, API design</b></summary>
<br />

- **ASP.NET Core** (Web API & MVC) on modern .NET — minimal APIs, middleware, background services
- **EF Core** against SQL Server and PostgreSQL — migrations, compiled queries, split queries, killing N+1
- **API design** — versioning, FluentValidation, ProblemDetails, OpenAPI contracts that clients can trust

</details>

<details>
<summary><b>🎨 Frontend &nbsp;—&nbsp; Blazor, React, Angular, Vue</b></summary>
<br />

- **Blazor** Server & WebAssembly — component design, render modes, JS interop
- **React / Angular / Vue** wired to .NET APIs with typed clients generated from OpenAPI
- HTML5, CSS3, **TypeScript**, responsive layouts and accessible markup

</details>

<details>
<summary><b>☁️ Cloud &amp; DevOps &nbsp;—&nbsp; Azure, Docker, CI/CD</b></summary>
<br />

- **Azure** — App Service, Functions, Container Apps, Key Vault, Application Insights
- **Docker** multi-stage builds; slim runtime images, health checks, sane layer caching
- **CI/CD** with GitHub Actions and Azure DevOps — build, test, scan, deploy on every push

</details>

<details>
<summary><b>⚡ Performance &nbsp;—&nbsp; the part most people skip</b></summary>
<br />

- Query and **index tuning** driven by execution plans, not guesswork
- Fixing **N+1** and over-eager `Include` chains before they reach production
- **Caching** layers that actually invalidate: output caching, `IDistributedCache`, Redis
- Benchmarking with **BenchmarkDotNet** so "faster" is a number, not a feeling

</details>

<details>
<summary><b>🛡️ Security &nbsp;—&nbsp; secure by default</b></summary>
<br />

- **ASP.NET Core Identity**, JWT and cookie auth, policy-based authorisation
- Defence against **XSS, CSRF, SQL injection** and IDOR — parameterised everything, authorise every handler
- Secrets in **Key Vault**, never in `appsettings.json`

</details>

<details>
<summary><b>🧪 Testing &nbsp;—&nbsp; so refactors aren't scary</b></summary>
<br />

- **xUnit / NUnit** with **Moq** or NSubstitute for unit tests
- Integration tests via **`WebApplicationFactory`** and **Testcontainers** against a real database
- Tests wired into CI — a red build blocks the merge

</details>

<!--
## 🚀 Featured projects

Điền 2–4 repo tiêu biểu vào đây rồi bỏ comment block này.
Card bên dưới tự render tên repo, mô tả và ngôn ngữ — chỉ cần đổi `repo=`.
Nếu chưa có gì để khoe thì cứ để nguyên trong comment: một section trống
còn tệ hơn là không có section.

<div align="center">
  <a href="https://github.com/phuongfullstack/REPO-NAME">
    <img src="https://github-readme-stats.vercel.app/api/pin/?username=phuongfullstack&repo=REPO-NAME&theme=tokyonight&hide_border=true&border_radius=10" alt="REPO-NAME" />
  </a>
  <a href="https://github.com/phuongfullstack/OTHER-REPO">
    <img src="https://github-readme-stats.vercel.app/api/pin/?username=phuongfullstack&repo=OTHER-REPO&theme=tokyonight&hide_border=true&border_radius=10" alt="OTHER-REPO" />
  </a>
</div>
-->

---

## 📊 GitHub

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats.vercel.app/api?username=phuongfullstack&show_icons=true&rank_icon=github&hide_border=true&border_radius=10&theme=tokyonight" />
  <source media="(prefers-color-scheme: light)" srcset="https://github-readme-stats.vercel.app/api?username=phuongfullstack&show_icons=true&rank_icon=github&hide_border=true&border_radius=10&theme=default" />
  <img src="https://github-readme-stats.vercel.app/api?username=phuongfullstack&show_icons=true&rank_icon=github&hide_border=true&border_radius=10&theme=tokyonight" alt="GitHub stats for phuongfullstack" />
</picture>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats.vercel.app/api/top-langs/?username=phuongfullstack&layout=compact&langs_count=8&hide_border=true&border_radius=10&theme=tokyonight" />
  <source media="(prefers-color-scheme: light)" srcset="https://github-readme-stats.vercel.app/api/top-langs/?username=phuongfullstack&layout=compact&langs_count=8&hide_border=true&border_radius=10&theme=default" />
  <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=phuongfullstack&layout=compact&langs_count=8&hide_border=true&border_radius=10&theme=tokyonight" alt="Most used languages by phuongfullstack" />
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://streak-stats.demolab.com?user=phuongfullstack&hide_border=true&border_radius=10&theme=tokyonight" />
  <source media="(prefers-color-scheme: light)" srcset="https://streak-stats.demolab.com?user=phuongfullstack&hide_border=true&border_radius=10&theme=default" />
  <img src="https://streak-stats.demolab.com?user=phuongfullstack&hide_border=true&border_radius=10&theme=tokyonight" alt="Contribution streak for phuongfullstack" />
</picture>

</div>

### 🐍 Contribution graph

<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/phuongfullstack/phuongfullstack/output/github-snake-dark.svg" />
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/phuongfullstack/phuongfullstack/output/github-snake.svg" />
    <img src="https://raw.githubusercontent.com/phuongfullstack/phuongfullstack/output/github-snake.svg" alt="Snake eating the contribution graph of phuongfullstack" />
  </picture>
</div>

---

<div align="center">

## 💬 Get in touch

Happy to talk about .NET architecture, a query that got slow, or a project you're planning.

<a href="https://linkedin.com/in/phuongfullstack"><img src="https://img.shields.io/badge/Message_me_on_LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="Message me on LinkedIn" /></a>

<img src="assets/footer.svg" width="100%" alt="" />

</div>
