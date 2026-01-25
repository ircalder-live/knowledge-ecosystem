Sprint 03 — Mid‑Sprint Review
Project: Knowledge Ecosystem
Sprint: 03
Date: [insert date]  
Owner: Ian
Purpose: Mid‑sprint checkpoint to evaluate divergence from the Sprint 03 Initiation Document, record the GitHub disruption, document the scope refactor, and establish the updated trajectory for the remainder of the sprint.

1. Context and Summary
This mid‑sprint review replaces the originally planned ceremony due to a significant platform disruption.  
* GitHub instability prevented the establishment of quantitative governance via issue transitions.  
* Downstream sprint items dependent on GitHub telemetry were disrupted.  
* A local‑first, sovereign telemetry architecture emerged as the new foundation.  
* Sprint 03 remains active, but its scope and execution model have been refactored. This mid-sprint review demonstrates that the sprint remains intact and on track.  

2. Original Intent (from Initiation Document)

2.1 Baselines Carried Forward
* Velocity baseline
* Experimentation baseline
* Domain baseline
* Governance baseline

2.2 Quantitative Governance Plan
* Cycle time, lead time, throughput
* Slack, WIP, dependency latency
* GitHub‑based telemetry

2.3 Capacity Planning
* Expected throughput  
* Expected experiment load  
* Domain artifacts  
* Governance automation task  

2.4 Sprint Theme
Quantitative governance, automation, and domain deepening.

2.5 Sprint Goals
* Metrics extractor  
* Dashboard generator  
* Governance report  
* MLflow integration  
* AzureML integration  
* Governance Automation domain  

2.6 Scope & Deliverables
* GitHub API scripts  
* GitHub Actions  
* Governance datasets  
* MLflow experiment  
* AzureML dataset/pipeline  
* Domain artifacts  

2.7 Risks & Mitigations
* Over‑engineering  
* AzureML complexity  
* MLflow friction  
* Scope creep  
* Visualization complexity  

3. Disruption Analysis (GitHub as Inflection Point)

Our goal was to extract essential governance metrics from GitHub, as recorded through that project and issues operations board and other related screens. This was well-developed during Sprint 02. We expected insightful data to be extracted through the API. We wrote a script to do so. That script returned repeated null values for key fields. We realized that the metrics were being denied and the type of project persisted as an individual (V1) project.
### GitHub ProjectsV2 instability
We made several attempts to initiate a V2 Project in GitHub, both through the web interface and the CLI. After several attempts, we realized there was no solution that enabled a V2 project with a free organization account or individual account. These features had been (silently) removed from such accounts. There was no such discussion in the relevant GitHub blogs or change logs. There were no indications anywhere on any of the screens or CLI. By trial and error, costing much time and effort, we came to this realization.

###  Inability to rely on issue transitions for telemetry
We were also unable to rely on issue transitions from the Backlog, through In Progress, to Review and Done for telemetry of a quality necessary for governance. 
###  Loss of quantitative governance substrate
Taken together, these instabilities are systemic (not incidental), thereby disabling the sprint's core measuremant substrate. This situation meant that GitHub could not provide the quantitative governance substrate that we envisaged. Another such substrate became necessary.  
### Downstream disruption to metrics extractor, dashboards, and automation
Due to the dependencies upon developing a capable data extractor from the GitHub API, not only the extractor, but also the downstream metrics dashboards and automation were disrupted. This threatened the collapse of the entire sprint.  
### Decision to deprecate GitHub as a planning surface
GitHub handed us a dilemma: Either pay for the tier of account that can actually do V2 projects, or do without those GitHub services. These behaviors from GitHub; the lack of transparency about ProjectsV2, the restriction of the API to collect and return the project data that we generated with our actions (effectively holding our own data for ransom), the silent removal of previously available features, the absence of any kind of notifications, leaving us to discover for ourselves what was missing, were clear signals of unethical monetization conditions and efforts we would not support. GitHub's behavior introduced governance risk, not just inconvenience.
### Migration to local‑first governance telemetry
Understanding that git itself creates timestamped records of commits, and that we had good commit messages, with clear sprint boundaries, bursts and issues, we surmised that we could reconstruct our own governance metrics and project telemetry from these local data. Therefore, we pivoted to local-first governance telemetry. We constructed a script that parsed the .git data into csv and parquet data files. We developed a Notebook that was able to generate governance quality metrics and visualizations. These are derived directly from the data, without any vendor filtering, manipulations, summarizations, interpretations, or other distortions.  
These results enable us to recover Sprint 03 in a technologically and methodologically superior architecture than what was originally envisaged. With this migration to local-first governance telemetry, we are in a strong position to recover Sprint 03, with perhaps greater strategic advancement than originally intended. We will refactor the scope of Sprint 03 accordingly with such ambition.

4. Scope Refactoring Summary
A table capturing the fate of each original scope item.

4.1 Scope Item Status Table
<table>
  <thead>
    <tr>
      <th>Original Scope Item</th>
      <th>Status</th>
      <th>Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>GitHub metrics extractor</td>
      <td>Deprecated</td>
      <td>Replaced by local-first telemetry</td>
    </tr>
    <tr>
      <td>Dashboard generator</td>
      <td>Refactored</td>
      <td>Notebook-based visualization</td>
    </tr>
    <tr>
      <td>Governance report</td>
      <td>Deferred</td>
      <td>Candidate for Sprint 04</td>
    </tr>
    <tr>
      <td>MLflow integration</td>
      <td>Achieved</td>
      <td>Now foundational</td>
    </tr>
    <tr>
      <td>AzureML integration</td>
      <td>Deferred</td>
      <td>Out of Sprint 03 scope</td>
    </tr>
    <tr>
      <td>Governance Automation domain</td>
      <td>In progress</td>
      <td>Local scaffolding</td>
    </tr>
    <tr>
      <td>Domain artifacts</td>
      <td>Deferred</td>
      <td>To Sprint 04</td>
    </tr>
    <tr>
      <td>Documentation hygiene</td>
      <td>Achieved</td>
      <td>Ongoing</td>
    </tr>
  </tbody>
</table>

5. Updated Risk Assessment
Re-evaluate the original risks:

5.1 Realized Risks
Platform instability (GitHub)

AzureML complexity (deferred)

5.2 Mitigated Risks

* Over‑engineering (local-first minimalism)  
* MLflow friction (resolved through adoption)  
* Visualization complexity (simplified via notebook)
* Vendor lock-in risk, realized, mitigated via local-first architecture

5.3 New Risks

None significant; architecture now more stable than before.

6. New Architecture (Post‑Refactor)
Document the structural pivot:

6.1 Planning Substrate
GitHub is no longer used for issues, projects, or workflow management
New architecture is extensible, able to grow without platform constraints.

Local schemas for:

* Sprints  
* Issues  
* Tasks  

6.2 Telemetry Substrate

* MLflow for runs and experiments  
* Local CSV/Parquet for governance metrics  
* Notebook for dashboards and time‑series analysis  

6.3 Conceptual Mapping  

* Sprint → tag

* Issue → MLflow experiment

* Task → MLflow run

6.4 Governance Benefits  
* Sovereignty
* Reproducibility
* Traceability
* Platform independence

7. Remaining Work for Sprint 03
A crisp list of what remains achievable within the sprint boundary:

* Finalize GitHub deprecations (completed)  
* Update local sprint artifacts (initiation.md, telemetry logs)  
* Create sprints, issues, tasks schemas  
* Add initial entries to the new schemas (Sprints, Issues, Tasks)
* Initialize MLflow locally  
* Validate end‑to‑end telemetry flow  
* Begin local time‑series generation  
* Prepare Sprint 03 closure note  
* Prepare Sprint 04 intake list  

8. Implications for Sprint 04
Capture what Sprint 04 will inherit:
* Local-first governance telemetry  
* MLflow-based experimentation  
* Refactored scope items  
* Domain artifacts deferred from Sprint 03  
* Governance Automation domain backlog  
* AzureML integration (if still desired)  
This is not planning — just intake.

9. Reflection and Governance Notes
A short reflective section:
**What was learned**
Vendor dependencies are precarious. Vendors have their own agendas and managers of varying alignment or awareness of customer needs. We have seen clueless behavior and wanton disregard of their impacts by their silent feature removals. The importance of retaining data sovereignty and regarding the behaviors and decisions (track record) of vendors and platforms has been demonstrated (again). Adaptability to, or avoidance of such instabilities enables continuation in the face of disruptions.
**What was strengthened**
We now have a superior architecture for this and future sprints. Our ability to progress is enhanced. We have platform independence and fewer constraints or dependencies. The fact that our new telemetry pipeline is fully reconstructable from git history is a major governance advantage.  
**How the sprint adapted**
The sprint adapted by developing an alternative source of governance telemetry data that is local and independent of any external party or vendor. This data source is readily available and completely understood. Experiments and initial developement (data and notebook) readily produced governance-grade results. These results enabled the adaptation of the sprint to this new local-first governance telemetry. 
**How governance integrity was preserved**
We can now define and apply our own telemetry objects as we see fit for governance. This preserves and actually strengthens governance integrity by retaining our own control over telemetry, metrics and measures, as our own sovereign data. Our data and experiments are actually more reproducible and traceable than was previously possible, given the vendor constraints. 
**Why the refactor improved the ecosystem**
We now have an architecture that is open and completely within our direction and discretion. The architecture itself is actually more resilient and adaptable, as we are freed from (arbitrary) API restrictions, which have shown themselves to be real risks and impediments. The ecosystem is free to grow and evolve as we think best, with complete auditability and transparency (i.e. no black boxes). The architecture is simpler, easier to diagnose and manage, with fewer potential points of failure, and multiple options for extension and adaptation. 

10. Mid‑Sprint Review Conclusion
This mid-sprint review has come at a significant time, not only for the sprint, but for the entire project and ecosystem. We can now affirm:
* Sprint 03 remains on track under the refactored scope  
* The new architecture is stable and sovereign  
* The sprint will close cleanly and intentionally  
* Sprint 03 will close with a clear boundary and a stable foundation for Sprint 04
* Sprint 04 will begin with clarity and momentum.