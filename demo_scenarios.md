# Demo Scenarios: Near-Miss Reporter

## Scenario 1: End-to-End Reporting & AI Insight
**Objective**: Show the core value proposition: easy reporting and intelligent analysis.
**Steps**:
1. Log in to the application as a standard user.
2. Click **Add Report** and enter a realistic near-miss scenario (e.g., "Forklift carrying pallet almost collided with pedestrian at blind corner in Warehouse B").
3. Submit the report and observe the real-time update on the dashboard and toast notification.
4. Open the **AI Insights** panel and click **Analyze Current Page**.
5. Read aloud the generated recommendation, highlighting how the AI identifies the root cause (blind corner) and suggests immediate actions (install convex mirrors).
**Talking Points**:
- "Notice how quickly a user can submit a report without friction."
- "The AI service immediately processes the text, providing actionable insights that would normally take hours of safety committee review."

## Scenario 2: Data Import & Analytics
**Objective**: Demonstrate bulk data handling and visual reporting.
**Steps**:
1. Click the **Import CSV** button.
2. Select `sample_reports.csv` and upload it.
3. Observe the success notification and the sudden increase in KPI numbers on the dashboard.
4. Navigate to the **Analytics Dashboard**.
5. Switch the period selector to "Last 30 Days" and point out the dynamic Recharts graphs.
**Talking Points**:
- "We understand that data often comes from legacy systems, so we built robust CSV ingestion with type and size validation."
- "Our dashboard instantly visualizes this data, giving management a bird's-eye view of incident trends and severity distributions."

## Scenario 3: Security & Audit Logging
**Objective**: Prove enterprise-grade security and compliance.
**Steps**:
1. Navigate to the terminal/Postman to demonstrate an unauthenticated request to the API.
2. Show the `401 Unauthorized` response to prove token-based security is enforced.
3. Attempt a SQL injection payload via the frontend (`' OR 1=1 --`) and show the `400 Bad Request` block.
4. Delete a report from the UI.
5. Show the database `audit_log` table (or explain it) capturing the "DELETE" action with timestamps and user info.
**Talking Points**:
- "Security is not an afterthought. We enforce strict JWT token validation and sanitize all inputs against XSS and SQL injection."
- "Through Spring AOP, every Create, Update, and Delete action is silently logged in our audit trails, ensuring complete compliance with safety regulations."
