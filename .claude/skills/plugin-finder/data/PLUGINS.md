# Claude Code Official Plugin Registry

> **Source:** [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official)
> **Last Updated:** 2025-12-29
> **Total Plugins:** 40 (22 internal, 18 external)

This registry documents all plugins available in Anthropic's official Claude Code plugin marketplace. Plugins are divided into two categories: **internal** plugins developed and maintained by Anthropic, and **external** plugins provided by third-party partners via MCP (Model Context Protocol) servers.

---

## External Partner Plugins (MCP Servers)

These plugins connect Claude Code to external services via the Model Context Protocol. They are maintained by their respective providers but curated by Anthropic for inclusion in the official marketplace.

| Plugin | Provider | Stars | Maintenance | Repository |
|--------|----------|-------|-------------|------------|
| [Context7](#context7) | Upstash | 40,409 | Very Active | [upstash/context7](https://github.com/upstash/context7) |
| [GitHub](#github) | GitHub | 25,504 | Very Active | [github/github-mcp-server](https://github.com/github/github-mcp-server) |
| [Serena](#serena) | Oraios | 17,856 | Very Active | [oraios/serena](https://github.com/oraios/serena) |
| [Stripe](#stripe) | Stripe | 1,176 | Active | [stripe/ai](https://github.com/stripe/ai) |
| [Atlassian](#atlassian) | Atlassian | 167 | Active | [atlassian/atlassian-mcp-server](https://github.com/atlassian/atlassian-mcp-server) |
| [Figma](#figma) | Figma | 110 | Active | [figma/mcp-server-guide](https://github.com/figma/mcp-server-guide) |
| [Greptile](#greptile) | Greptile | 18 | Active | [sosacrazy126/greptile-mcp](https://github.com/sosacrazy126/greptile-mcp) |
| [Notion](#notion) | Notion | 9 | New | [makenotion/claude-code-notion-plugin](https://github.com/makenotion/claude-code-notion-plugin) |
| [Sentry](#sentry) | Sentry | 3 | New | [getsentry/sentry-for-claude](https://github.com/getsentry/sentry-for-claude) |
| [Vercel](#vercel) | Vercel | 2 | New | [vercel/vercel-deploy-claude-code-plugin](https://github.com/vercel/vercel-deploy-claude-code-plugin) |
| [Playwright](#playwright) | Microsoft | - | Active | [Plugin Source](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/playwright) |
| [Supabase](#supabase) | Supabase | - | Active | [Plugin Source](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/supabase) |
| [Firebase](#firebase) | Google | - | Active | [Plugin Source](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/firebase) |
| [Linear](#linear) | Linear | - | Active | [Plugin Source](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/linear) |
| [Asana](#asana) | Asana | - | Active | [Plugin Source](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/asana) |
| [Slack](#slack) | Slack | - | Active | [Plugin Source](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/slack) |
| [GitLab](#gitlab) | GitLab | - | Active | [Plugin Source](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/gitlab) |
| [Laravel Boost](#laravel-boost) | Community | - | Active | [Plugin Source](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/laravel-boost) |

### Maintenance Status Legend

| Status | Description |
|--------|-------------|
| Very Active | Commits within the last week, active issue response, large community |
| Active | Regular commits within the last month, stable development |
| New | Recently created plugin, limited history but actively developed |
| Maintained | Periodic updates, stable codebase |
| Stale | No recent activity, may be abandoned |

---

## External Plugin Details

### Context7

**Provider:** Upstash | **Stars:** 40,409 | **Category:** Exploration
**Repository:** https://github.com/upstash/context7

Context7 is a documentation lookup MCP server that has quickly become one of the most popular plugins in the ecosystem. It solves a critical problem for AI coding assistants: accessing up-to-date, version-specific documentation directly within the LLM context.

Rather than relying on potentially outdated training data, Context7 pulls documentation and code examples directly from source repositories in real-time. This means when you're working with a library, you get the exact documentation for the version you're using, not a stale snapshot. The server supports thousands of libraries and frameworks, making it invaluable for modern polyglot development.

The plugin provides two primary tools: `resolve-library-id` for finding the correct library identifier, and `query-docs` for retrieving relevant documentation sections. It's particularly useful when exploring unfamiliar APIs or when library documentation has been updated since Claude's training cutoff.

---

### GitHub

**Provider:** GitHub | **Stars:** 25,504 | **Category:** Productivity
**Repository:** https://github.com/github/github-mcp-server

GitHub's official MCP server is the definitive integration for repository management within Claude Code. Written in Go, it provides comprehensive access to GitHub's API, enabling Claude to create and manage issues, handle pull requests, review code, search across repositories, and interact with virtually any aspect of your GitHub workflow.

This plugin transforms Claude Code into a first-class GitHub citizen. You can create issues from code comments, generate pull request descriptions, search for relevant code across your organization, and manage repository settings without leaving your terminal. The server handles authentication through personal access tokens or GitHub Apps, supporting both individual developers and enterprise deployments.

With over 25,000 stars, it's one of the most actively developed MCP servers in the ecosystem. GitHub maintains it alongside their core platform, ensuring API compatibility and feature parity as GitHub evolves. The 250+ open issues reflect active community engagement rather than neglect, with rapid response times from GitHub's team.

---

### Serena

**Provider:** Oraios | **Stars:** 17,856 | **Category:** Exploration
**Repository:** https://github.com/oraios/serena

Serena represents a fundamentally different approach to AI-assisted coding. Rather than relying on text-based pattern matching like most tools, Serena provides semantic code analysis through deep language server protocol integration. This gives Claude genuine understanding of your codebase's structure, not just string matching.

The plugin supports over 30 programming languages through its LSP abstraction layer, including Python, JavaScript, TypeScript, Rust, Go, Java, C/C++, and Ruby. When you ask about code, Serena can trace symbol definitions, understand type hierarchies, navigate inheritance chains, and suggest refactorings that respect your codebase's semantic structure.

What makes Serena unique is its positioning as a free alternative to expensive coding assistants. By operating as an MCP server, it bypasses API costs while providing IDE-level intelligence. The JetBrains plugin integration allows it to leverage your IDE's analysis capabilities, making it particularly powerful for complex enterprise codebases where context is everything.

Serena is community-managed but actively maintained, with 17,000+ stars reflecting its importance in the ecosystem. For challenging coding tasks where understanding structure matters more than finding text, Serena is often the difference between useful assistance and frustrating hallucinations.

---

### Stripe

**Provider:** Stripe | **Stars:** 1,176 | **Category:** Development
**Repository:** https://github.com/stripe/ai

Stripe's AI repository is their one-stop shop for building AI-powered payment products. The Claude Code plugin component enables direct integration with Stripe's payment infrastructure, letting you build and test payment flows without constant context-switching.

This plugin is particularly valuable for developers building e-commerce, SaaS, or marketplace applications. Claude can help you implement checkout flows, subscription management, webhook handlers, and payment intent workflows with direct access to Stripe's API patterns and best practices. The integration understands Stripe's object model and can guide you through proper error handling, idempotency patterns, and test mode workflows.

With Stripe's emphasis on developer experience, this plugin benefits from the same attention to detail that makes their API documentation legendary. Whether you're implementing your first payment form or debugging a complex multi-party payment flow, having Stripe's tools directly in Claude Code accelerates development significantly.

---

### Atlassian

**Provider:** Atlassian | **Stars:** 167 | **Category:** Productivity
**Repository:** https://github.com/atlassian/atlassian-mcp-server

The Atlassian MCP server bridges Claude Code with Jira and Confluence, two cornerstones of enterprise software development. This Python-based plugin enables secure connections between your development workflow and Atlassian's collaboration ecosystem.

For teams using Jira, this means Claude can create and search issues, manage sprints, update ticket statuses, and pull in issue context while you code. When you're fixing a bug, Claude can fetch the relevant Jira ticket, understand the reported behavior, and help you craft a commit message that properly references the issue.

Confluence integration brings documentation into your development flow. Claude can search your team's knowledge base, pull relevant technical specs, and even help update documentation based on code changes. For enterprises where Atlassian is the source of truth, this plugin makes Claude Code a first-class participant in your workflow rather than an isolated tool.

The 167 stars and 18 open issues indicate active development and community engagement, with Atlassian treating this as a supported integration rather than an experiment.

---

### Figma

**Provider:** Figma | **Stars:** 110 | **Category:** Design
**Repository:** https://github.com/figma/mcp-server-guide

Figma's MCP server guide provides the integration layer between design and development. This plugin enables Claude to access design files, extract component information, read design tokens, and translate visual designs into code.

The design-to-code gap has traditionally been one of the most friction-filled parts of frontend development. Designers create beautiful mockups, then developers manually translate them into CSS, components, and layouts. Figma's integration lets Claude see the actual design specifications, spacing values, color tokens, and component structure, producing code that more accurately reflects the intended design.

This is particularly powerful for design systems work, where consistency matters. Claude can extract the exact values from Figma's design tokens, ensuring your implementation matches the source of truth. For component development, it can see the intended states, variants, and responsive behaviors directly in the design file.

The plugin is still relatively new (110 stars) but represents Figma's commitment to closing the design-development gap through AI assistance.

---

### Greptile

**Provider:** Greptile | **Stars:** ~18 | **Category:** Exploration
**Repository:** https://github.com/sosacrazy126/greptile-mcp

Greptile provides AI-powered codebase search and understanding through natural language queries. Instead of constructing complex regex patterns or navigating file trees, you can ask questions about your codebase in plain English.

The plugin excels at architectural questions: "Where are API endpoints defined?", "How does authentication flow through the application?", "What uses this deprecated function?" Greptile's AI understands code semantics, not just text patterns, so it can answer questions about relationships, dependencies, and code flow.

Note that the community-maintained MCP wrapper listed here may differ from Greptile's official implementation. Greptile (the company) raised $25M in Series A funding in late 2025, indicating significant investment in their core technology. The official Greptile service includes features like auto-resolving PR comments and deep code analysis that may not be fully represented in the open-source MCP server.

For teams wanting AI-powered code search without API costs, this MCP integration provides a solid foundation, though enterprises may want to evaluate Greptile's full commercial offering.

---

### Notion

**Provider:** Notion | **Stars:** 9 | **Category:** Productivity
**Repository:** https://github.com/makenotion/claude-code-notion-plugin

Notion's official Claude Code plugin connects your development workflow to Notion's workspace platform. Search pages, create and update documents, manage databases, and access your team's knowledge base directly from Claude Code.

For teams using Notion as their documentation hub, this integration is transformative. Claude can fetch relevant technical documentation while you code, update specs based on implementation decisions, and ensure your knowledge base stays synchronized with your codebase. The bidirectional nature means Claude isn't just reading from Notion; it can actively contribute to your documentation.

The plugin supports Notion's database features, enabling Claude to interact with structured data like project trackers, feature requests, or bug databases. Combined with code context, this creates powerful workflows where Claude can cross-reference implementation status with project documentation.

At just 9 stars, this is a new plugin with limited community feedback, but it's maintained by Notion themselves, ensuring long-term viability and API compatibility.

---

### Sentry

**Provider:** Sentry | **Stars:** 3 | **Category:** Monitoring
**Repository:** https://github.com/getsentry/sentry-for-claude

Sentry's error monitoring integration brings production error context directly into your development environment. Access error reports, analyze stack traces, search issues by fingerprint, and debug production errors without leaving Claude Code.

When you're investigating a bug, context is everything. Sentry's plugin lets Claude fetch the actual error reports from production, including stack traces, breadcrumbs, user context, and affected sessions. This transforms debugging from guesswork into informed analysis, as Claude can see exactly what happened in production when the error occurred.

The plugin supports Sentry's issue search, letting you find related errors, track regressions, and understand error patterns across your application. For teams practicing observability-driven development, having error monitoring data in your AI assistant's context is a significant productivity boost.

This is a brand-new plugin (3 stars, created November 2025) marked as production-ready by Sentry. Expect rapid iteration as Sentry refines the integration based on early adopter feedback.

---

### Vercel

**Provider:** Vercel | **Stars:** 2 | **Category:** Deployment
**Repository:** https://github.com/vercel/vercel-deploy-claude-code-plugin

Vercel's deployment plugin brings infrastructure control into Claude Code. Manage deployments, check build status, access logs, configure domains, and control your frontend infrastructure directly from your development workflow.

For teams on Vercel, this eliminates constant context-switching between your terminal and the Vercel dashboard. Claude can check deployment status, pull build logs when something fails, preview environment URLs, and help troubleshoot deployment issues with full context of what's happening in your infrastructure.

The integration is particularly powerful for Vercel's preview deployments, where each pull request gets its own environment. Claude can fetch the preview URL, check its status, and help you iterate on changes with immediate feedback from the deployed environment.

Created December 2025, this is Vercel's newest integration with just 2 stars. As with Sentry, expect rapid development as Vercel responds to early user feedback.

---

### Playwright

**Provider:** Microsoft | **Category:** Testing
**Plugin Source:** [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/playwright)

Microsoft's Playwright MCP server enables browser automation and end-to-end testing directly through Claude Code. Claude can interact with web pages, take screenshots, fill forms, click elements, and execute automated browser testing workflows.

This transforms how you develop and test frontend applications. Rather than manually clicking through flows or writing test scripts from scratch, you can describe what you want to test and have Claude generate and execute Playwright tests in real-time. See a visual bug? Claude can navigate to the page, take a screenshot, and help you identify the styling issue.

Playwright's cross-browser support means Claude can test across Chromium, Firefox, and WebKit, catching browser-specific issues before they reach production. The MCP integration makes this capability accessible without leaving your development workflow.

---

### Supabase

**Provider:** Supabase | **Category:** Database
**Plugin Source:** [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/supabase)

The Supabase MCP integration provides comprehensive access to Supabase's backend-as-a-service platform. Manage Firestore databases, authentication, storage, and real-time subscriptions directly from Claude Code.

For developers building on Supabase, this means Claude can help you write and execute SQL queries, manage row-level security policies, configure authentication providers, and work with storage buckets without switching contexts. The integration understands Supabase's architecture, helping you implement proper patterns for real-time subscriptions and auth flows.

This is particularly powerful for rapid prototyping, where you can describe a feature and have Claude implement the full stack from database schema to API integration, with direct access to verify and test each component in Supabase.

---

### Firebase

**Provider:** Google | **Category:** Database
**Plugin Source:** [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/firebase)

Google's Firebase MCP integration connects Claude Code to Firebase's comprehensive backend platform. Manage Firestore databases, authentication, cloud functions, hosting, and storage within your development workflow.

Firebase's NoSQL document model and real-time capabilities require specific patterns and best practices. This integration gives Claude direct access to your Firebase project, enabling it to understand your data structure, suggest query optimizations, and help implement security rules that match your application's access patterns.

For cloud functions development, Claude can test function logic, check deployment status, and help debug issues with full context of your Firebase environment. The hosting integration enables rapid iteration on static deployments, with Claude able to check deployment status and preview URLs.

---

### Linear

**Provider:** Linear | **Category:** Productivity
**Plugin Source:** [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/linear)

Linear's issue tracking integration brings modern project management into Claude Code. Create issues, manage projects, update statuses, search across workspaces, and streamline your development workflow with Linear's fast, keyboard-driven interface philosophy.

Linear has become the issue tracker of choice for many startups and modern engineering teams, prized for its speed and developer-friendly design. This integration extends that philosophy into AI-assisted development, where Claude can create issues from code comments, update ticket status as you work, and pull in issue context when you need it.

The search capabilities are particularly valuable for large projects, letting Claude find related issues, understand feature scope, and help you navigate your team's work history without leaving your terminal.

---

### Asana

**Provider:** Asana | **Category:** Productivity
**Plugin Source:** [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/asana)

Asana's project management integration connects enterprise work management to Claude Code. Create and manage tasks, search projects, update assignments, and track progress across your organization's work.

For teams where Asana is the system of record, this plugin ensures Claude has visibility into project context, deadlines, and task dependencies. Claude can create tasks for follow-up work discovered during coding, update task status as features are completed, and help you understand how your current work fits into broader project timelines.

The integration supports Asana's project hierarchy, letting Claude navigate portfolios, projects, sections, and subtasks to find relevant context or create appropriately organized new work items.

---

### Slack

**Provider:** Slack | **Category:** Productivity
**Plugin Source:** [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/slack)

Slack's workspace integration brings team communication context into Claude Code. Search messages, access channels, read threads, and find relevant discussions while you're coding.

Development doesn't happen in isolation. Decisions are made in Slack threads, context is shared in channels, and important information lives in message history. This plugin gives Claude access to that context, helping it understand not just your code but the conversations that shaped it.

When you're implementing a feature, Claude can search for relevant Slack discussions to understand requirements, constraints, and decisions. When you're debugging an issue, it can find previous conversations about similar problems. The integration transforms Slack from a separate context into part of your development knowledge base.

---

### GitLab

**Provider:** GitLab | **Category:** Productivity
**Plugin Source:** [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/gitlab)

The GitLab integration provides comprehensive access to GitLab's DevOps platform. Manage repositories, merge requests, CI/CD pipelines, issues, and wikis through a unified MCP interface.

GitLab's all-in-one platform means this single integration covers what might require multiple plugins in other ecosystems. Claude can create and manage merge requests, check pipeline status, troubleshoot failing CI jobs, manage issues, and update documentation wikis, all within your development workflow.

For GitLab-centric organizations, this integration makes Claude a full participant in your DevOps lifecycle, from code to deployment.

---

### Laravel Boost

**Provider:** Community | **Category:** Development
**Plugin Source:** [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/laravel-boost)

Laravel Boost provides framework-specific assistance for Laravel applications. The MCP server understands Laravel's conventions, providing intelligent help with Artisan commands, Eloquent queries, routing, migrations, and Laravel-specific code generation.

Laravel's convention-over-configuration philosophy means there are "right ways" to do things in the framework. Laravel Boost encodes this knowledge, helping Claude generate code that follows Laravel best practices rather than generic PHP patterns. From proper migration structure to idiomatic Eloquent relationships, the plugin ensures Claude's Laravel output feels native to the framework.

This is particularly valuable for developers new to Laravel or for seasoned developers who want AI assistance that respects Laravel's patterns rather than fighting against them.

---

## Internal Anthropic Plugins

These plugins are developed and maintained directly by Anthropic. They don't require external MCP servers and run natively within Claude Code.

### Language Server Plugins

| Plugin | Description | Languages |
|--------|-------------|-----------|
| typescript-lsp | TypeScript/JavaScript language server for enhanced code intelligence | TS, JS, TSX, JSX |
| pyright-lsp | Python language server (Pyright) for type checking and code intelligence | Python |
| gopls-lsp | Go language server for code intelligence and refactoring | Go |
| rust-analyzer-lsp | Rust language server for code intelligence and analysis | Rust |
| clangd-lsp | C/C++ language server (clangd) with background indexing | C, C++ |
| php-lsp | PHP language server (Intelephense) for code intelligence | PHP |
| swift-lsp | Swift language server (SourceKit-LSP) for code intelligence | Swift |
| csharp-lsp | C# language server for code intelligence | C# |
| jdtls-lsp | Java language server (Eclipse JDT.LS) for code intelligence | Java |
| lua-lsp | Lua language server for code intelligence | Lua |

### Development Plugins

| Plugin | Description | Repository |
|--------|-------------|------------|
| agent-sdk-dev | Development kit for working with the Claude Agent SDK | [Link](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/agent-sdk-dev) |
| feature-dev | Comprehensive feature development workflow with specialized agents for codebase exploration, architecture design, and quality review | [Link](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/feature-dev) |
| frontend-design | Create distinctive, production-grade frontend interfaces with high design quality. Generates creative, polished code that avoids generic AI aesthetics | [Link](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/frontend-design) |
| ralph-wiggum | Interactive self-referential AI loops for iterative development. Claude works on the same task repeatedly, seeing its previous work, until completion | [Link](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/ralph-wiggum) |
| plugin-dev | Comprehensive toolkit for developing Claude Code plugins. Includes 7 expert skills covering hooks, MCP integration, commands, agents, and best practices | [Link](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/plugin-dev) |

### Productivity Plugins

| Plugin | Description | Repository |
|--------|-------------|------------|
| pr-review-toolkit | Comprehensive PR review agents specializing in comments, tests, error handling, type design, code quality, and code simplification | [Link](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/pr-review-toolkit) |
| commit-commands | Commands for git commit workflows including commit, push, and PR creation | [Link](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/commit-commands) |
| code-review | Automated code review for pull requests using multiple specialized agents with confidence-based scoring to filter false positives | [Link](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/code-review) |
| hookify | Easily create custom hooks to prevent unwanted behaviors. Define rules via simple markdown files | [Link](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/hookify) |

### Security & Learning Plugins

| Plugin | Description | Repository |
|--------|-------------|------------|
| security-guidance | Security reminder hook that warns about potential security issues when editing files, including command injection, XSS, and unsafe code patterns | [Link](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/security-guidance) |
| explanatory-output-style | Adds educational insights about implementation choices and codebase patterns | [Link](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/explanatory-output-style) |
| learning-output-style | Interactive learning mode that requests meaningful code contributions at decision points | [Link](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/learning-output-style) |

---

## Installation

Plugins from the official marketplace can be installed with:

```bash
# Install a specific plugin
/plugin install <plugin-name>

# List available plugins
/plugin list

# Search for plugins
/plugin search <query>
```

The official Anthropic marketplace is available by default. To explicitly add it:

```bash
/plugin marketplace add anthropics/claude-plugins-official
```

---

## Data Sources

- **Plugin Registry:** [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) (1,054 stars)
- **Claude Code:** [anthropics/claude-code](https://github.com/anthropics/claude-code) (49,602 stars)
- GitHub star counts and maintenance data retrieved 2025-12-29
