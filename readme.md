# Srifinder_bot

Telegram bot that use an specific project of **IRM** as core logic.

This bot allows you to:

1. Make inquiries.
2. Switch between the available datasets, with the `/change_dataset` command (currently CISI and CRAN).
3. Enable/Disable the use of **Roccio** in the queries, using the `/activate_roccio` and `/deactivate_roccio` commands.
4. From the results obtained with the queries, it is possible to download the selected document in _json_ format.
5. Download a `zip` file with the report and the source code of this implemented client of _IRM_.

## Configuration

This client is easy to configure, to be executed on a pc you must make sure that you have a `config.json` file in the root folder of the project, with a structure like the one shown below.

```json
{
  "api_token": "<bot-api-token>",
  "admins_uid": ["<your-telegram-user-id>", "<another-id>"]
}
```

enjoyit.
