# Workfront Fusion Automation

## Basics

### What is Workfront Fusion?
Workfront Fusion (formerly Integromat) is an automation platform that connects apps and services.
- Visual workflow builder (no-code / low-code)
- Supports 1000+ app integrations
- Runs scenarios on schedule or triggers
- Error handling and retry logic built-in

### Key Concepts
- **Scenario**: An automated workflow (sequence of modules)
- **Module**: A single action or trigger (e.g., "Watch new records")
- **Bundle**: A unit of data flowing through a scenario
- **Router**: Splits flow into multiple paths based on conditions
- **Iterator/Aggregator**: Loop over arrays or collect results

## Marketo Integration Patterns

### Sync Leads from Workfront to Marketo
1. Trigger: Watch new Workfront project or task
2. Map fields: project name → Marketo lead source
3. Create/Update lead in Marketo
4. Log result back to Workfront custom form

### Campaign Enrollment
- Use "Add Lead to List" module in Marketo
- Filter by lead score or status from Workfront
- Trigger email campaigns based on project milestones

### Common Marketo Modules
- `Watch Leads` - trigger on new/updated leads
- `Create/Update a Lead` - upsert lead record
- `Add Lead to List` - enroll in static list
- `Schedule Campaign` - trigger smart campaign
- `Get Lead by ID` - fetch lead details

## Campaign Setup Steps

### Step 1: Create Scenario
1. Go to Fusion > Scenarios > Create new scenario
2. Add trigger module (Workfront or Webhook)
3. Add Marketo modules for campaign actions

### Step 2: Configure Marketo Connection
1. In Fusion, go to Connections
2. Add new Marketo connection
3. Enter: Client ID, Client Secret, Munchkin ID
4. Test connection before saving

### Step 3: Map Data Fields
- Project Name → Campaign Name
- Due Date → Send Date
- Assigned User Email → Lead Email
- Custom form fields → Marketo custom fields

### Step 4: Test and Activate
1. Run scenario once manually
2. Check Marketo activity log
3. Verify data mapping is correct
4. Set schedule (hourly/daily/on event)
5. Activate scenario

## Common Issues and Solutions

### Issue: "Invalid Client Credentials" in Marketo
- Solution: Regenerate API credentials in Marketo Admin
- Check IP allowlist includes Fusion's IP ranges

### Issue: Scenario runs but no leads created
- Check field mapping (required fields: email, lastName)
- Verify Marketo partition permissions for API user
- Look at Fusion execution log for error bundles

### Issue: Duplicate leads in Marketo
- Use "Create or Update" (upsert) instead of "Create"
- Deduplicate by email field
- Add filter module before Marketo to check existing records

### Issue: Workfront webhook not triggering
- Verify webhook URL is correctly set in Workfront
- Check Workfront event subscription is active
- Use Fusion's "Run once" to test manually first

## Performance Tips
- Use filters early in the scenario to reduce bundle count
- Schedule heavy scenarios during off-peak hours
- Use data stores for cross-scenario data sharing
- Break large scenarios into sub-scenarios via HTTP modules
