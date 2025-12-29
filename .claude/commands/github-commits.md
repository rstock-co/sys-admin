# Generate Backdated GitHub Commits

Arguments: $ARGUMENTS

Parse the arguments as: `<start-date> <end-date> <num-commits>`

Example: `/github-commits 2024-01-01 2024-06-30 50`

## Task

1. Update `/home/neo/dev/github-bot/index.js` with the provided values:
   - Set `earliestDate` to the start date
   - Set `today` to the end date
   - Set the `makeCommit()` call to use the number of commits

2. Run `npm install` in the github-bot directory (if node_modules doesn't exist)

3. Run `npm start` to generate the commits

4. Report how many commits were created and the date range used
