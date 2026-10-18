<img alt="Hira Ahmed. AI Engineer and Systems QA Lead. Autonomous LLM pipelines that keep working." src="assets/hero.svg" width="100%">

<p align="center">
<a href="https://hiraahmed.me/"><img alt="Portfolio" src="assets/buttons/portfolio.svg" width="150"></a>
<a href="https://hiraahmed.me/Hira_Ahmed_Resume.pdf"><img alt="Resume" src="assets/buttons/resume.svg" width="150"></a>
<a href="mailto:hira229922@gmail.com"><img alt="Email" src="assets/buttons/email.svg" width="150"></a>
<a href="https://www.linkedin.com/in/hira-ahmed-4068402a7"><img alt="LinkedIn" src="assets/buttons/linkedin.svg" width="150"></a>
<a href="https://www.upwork.com/freelancers/~0178616a4e00b82166"><img alt="Hire me on Upwork" src="assets/buttons/hire.svg" width="150"></a>
</p>

<img alt="28K+ AI records enriched, 1,500+ defects documented, 34% monthly AWS cost cut, 83.81% SMT-verified repair" src="assets/stats.svg" width="100%">

I build AI automation, agents, and LLM pipelines that keep working when models, APIs, and data misbehave. Most of my work sits where AI meets backend and cloud engineering: n8n workflows, Python services, PostgreSQL state, and AWS. QA is the thread through all of it. I test the systems I build the way I test other people's: at the boundaries, at the API, and on the failure paths.

<br>

<img alt="01 Flagship work" src="assets/sections/flagship.svg" width="100%">

<p>
<a href="https://hiraahmed.me/case-studies/28k-record-pipeline/"><img alt="28K+ production AI enrichment pipeline" src="assets/cards/techpotion.svg" width="49%"></a>
<a href="https://hiraahmed.me/case-studies/cloud-compliance/"><img alt="Cloud compliance and AI auditing engine" src="assets/cards/compliance.svg" width="49%"></a>
</p>
<p>
<a href="https://hiraahmed.me/case-studies/multitenant-saas-qa/"><img alt="PharmaConnect multi-tenant B2B SaaS QA" src="assets/cards/pharma.svg" width="49%"></a>
<a href="https://hiraahmed.me/case-studies/sentinel-mesh/"><img alt="Sentinel-Mesh research" src="assets/cards/sentinel.svg" width="49%"></a>
</p>

<p align="center"><sub>Also: 34% monthly AWS cost reduction (Lambda, RDS PostgreSQL, API Gateway). Full archive at <a href="https://hiraahmed.me/case-studies/">hiraahmed.me</a></sub></p>

<img alt="02 Research" src="assets/sections/research.svg" width="100%">

**Sentinel-Mesh** remediates Terraform cloud-security misconfigurations. An LLM proposes a patch, a Z3 SMT verifier checks it against explicit security invariants, and a rejected patch's counterexample goes back to the model for another attempt. **The model only proposes. The verifier decides.**

<img alt="CloudFix-Bench results: Sentinel-Mesh 83.81%, no counterexample feedback 64.76%, Checkov baseline 35.24%" src="assets/research.svg" width="100%">

- **No security regressions observed** against the modeled invariants (0.0%, 95% interval 0.00% to 3.45%).
- **Scope:** formal guarantees hold only within the Cloud Perimeter Model. Properties outside it (WAF associations, logging policies) are checked without a proof certificate, and an external set of 12 cases reached 6/12.
- Lead author. Preprint on Research Square, manuscript under review. Peer reviewer for IEEE Access (5 verified reviews).

[Preprint](https://www.researchsquare.com/article/rs-10674271/latest) · [CloudFix-Bench on Zenodo](https://doi.org/10.5281/zenodo.20975067) · [Code](https://github.com/hira299/sentinel-mesh) · [Medium article](https://medium.com/@hira299/beyond-heuristics-formally-verifying-ai-generated-infrastructure-with-z3-smt-solvers-e95fd3a7bf95) · [Web of Science](https://www.webofscience.com/wos/author/record/QIV-1552-2026) · [ORCID](https://orcid.org/0009-0005-3219-7252)

<img alt="03 What I do" src="assets/sections/expertise.svg" width="100%">

<img alt="AI automation and agents, LLM pipelines and RAG, backend and cloud, QA and reliability" src="assets/pillars.svg" width="100%">

<p align="center"><sub>Python · FastAPI · PostgreSQL · n8n · LangGraph · LangChain · Groq · Gemini · AWS (EC2, Lambda, EventBridge, SQS, RDS, S3) · Terraform · Docker · Supabase</sub></p>

<img alt="04 Where I've worked" src="assets/sections/experience.svg" width="100%">

<img alt="QA Lead and Backend and Automation Engineer at TechPotion.ai, QA Intern at Sadiq.ai, Sentinel-Mesh research, B.S. Cybersecurity" src="assets/journey.svg" width="100%">

<img alt="05 Independent builds" src="assets/sections/builds.svg" width="100%">

| Project | What it shows |
|---|---|
| [AI-Autonomous-Email-Agent](https://github.com/hira299/AI-Autonomous-Email-Agent) | Stateful n8n email agent with per-thread memory and Groq inference |
| [Cloud-Security-Audit-Compliance-Automation-Platform](https://github.com/hira299/Cloud-Security-Audit-Compliance-Automation-Platform) | AWS audit pipeline with a persistent audit trail and a DLQ replay workflow |
| [Financial-Profitability-Guardrail](https://github.com/hira299/Financial-Profitability-Guardrail) | PostgreSQL state machine that alerts only on state transitions |
| [Autonomous-Competitor-Intelligence-SEO-Pipeline](https://github.com/hira299/Autonomous-Competitor-Intelligence-SEO-Pipeline) | Scheduled AI pipeline with defensive JSON parsing and a scraper DLQ |
| [Cloud-Cost-Sentinel](https://github.com/hira299/Cloud-Cost-Sentinel) | AWS cost anomaly detection with a rolling baseline |
| [vektor-ats-diagnostics](https://github.com/hira299/vektor-ats-diagnostics) | Multimodal document parsing and weighted evaluation engine |
| [browser-forensics-reconstruction](https://github.com/hira299/browser-forensics-reconstruction) | DFIR tool that reconstructs browser session timelines |
| [aegis-realtime-voice-dispatch](https://github.com/hira299/aegis-realtime-voice-dispatch) | Real-time voice command dispatch dashboard |

**Open resources:** [n8n-production-resilience-patterns](https://github.com/hira299/n8n-production-resilience-patterns) (retries, DLQs, idempotency, replay) · [enterprise-multitenant-qa-matrix](https://github.com/hira299/enterprise-multitenant-qa-matrix) (isolation, RBAC, API and business-logic test matrices)

<img alt="06 On GitHub" src="assets/sections/activity.svg" width="100%">

<p align="center">
<img alt="GitHub stats" src="https://github-readme-stats.vercel.app/api?username=hira299&count_private=true&include_all_commits=true&show_icons=true&hide_rank=true&hide_border=true&custom_title=GitHub&bg_color=151116&title_color=F4B8C8&text_color=9B9094&icon_color=C1304A" height="165">
<img alt="Most used languages" src="https://github-readme-stats.vercel.app/api/top-langs/?username=hira299&layout=compact&langs_count=6&hide_border=true&custom_title=Most%20used&bg_color=151116&title_color=F4B8C8&text_color=9B9094" height="165">
</p>

<p align="center">
<img alt="Contribution streak" src="https://streak-stats.demolab.com?user=hira299&hide_border=true&background=151116&stroke=2D2328&ring=C1304A&fire=F4B8C8&currStreakNum=EFE7E9&sideNums=EFE7E9&currStreakLabel=F4B8C8&sideLabels=9B9094&dates=9B9094" height="165">
</p>

<img alt="Contribution activity" src="https://github-readme-activity-graph.vercel.app/graph?username=hira299&area=true&hide_border=true&custom_title=Contribution%20activity&height=240&bg_color=0D1117&color=9B9094&title_color=F4B8C8&line=C1304A&point=F4B8C8&area_color=8E1F30" width="100%">

<img alt="Contribution snake" src="https://raw.githubusercontent.com/hira299/hira299/output/snake-dark.svg" width="100%">

<img alt="07 Let's talk" src="assets/sections/talk.svg" width="100%">

<a href="mailto:hira229922@gmail.com"><img alt="Need resilient AI pipelines or high-assurance QA? hira229922@gmail.com" src="assets/cta.svg" width="100%"></a>

<p align="center"><sub>Remote · 7:00 PM to 3:00 AM PKT, overlapping US/Canada hours and UK, Ireland, Germany afternoons · <a href="https://www.fiverr.com/hira299">Fiverr</a> · <a href="https://www.upwork.com/freelancers/~0178616a4e00b82166">Upwork</a> · <a href="https://topmate.io/hira_ahmed">Topmate</a> · <a href="https://www.researchgate.net/profile/Hira-Ahmed-28">ResearchGate</a></sub></p>
