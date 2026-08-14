# UE Voice Coverage Audit Contract

## Page status

| Status | Meaning | May test/report |
| --- | --- | --- |
| `active` | Current effective UE page or group | Yes |
| `deleted` | Marked 删除 or covered by a deletion region | No |
| `shelved` | Marked 搁置 | No |
| `deprecated` | Marked 废弃 or superseded | No |
| `draft` | Draft-only material | No |
| `backup` | Backup/history copy | No |
| `status_conflict` | Structural and visual status disagree | No |

Record the exact visual/layer evidence for every non-active status.

## Voice verdict

| Verdict | Meaning | Report to sheet |
| --- | --- | --- |
| `pass` | Executable operation matches UE target, action, and required value | No |
| `unsupported` | Platform returns an unsupported intent | Yes |
| `misrouted` | Operation targets another function or performs another action | Yes |
| `empty_required_slot` | Required canonical/target/action/value/channel is empty | Yes |
| `chat_only` | Only conversational text is returned | Yes |
| `blocked` | Platform blocks a valid UE action | Yes |
| `gui_only` | Only opens GUI when direct execution is required | Yes |
| `ambiguous` | Evidence is insufficient or paraphrases conflict | No; investigate |

`classification: task` is not proof of success. Inspect every operation and parameter.

## Manifest shape

```json
{
  "module": "情景模式",
  "vehicle": "8295",
  "alchemy_environment": "BIGSUR",
  "pages": [
    {
      "id": "543:123",
      "name": "3.情景模式-恒温座舱",
      "status": "deleted",
      "evidence": "V1.9 canvas red deletion region"
    }
  ],
  "controls": [
    {
      "id": "sleep-seat-entry",
      "page_id": "543:456",
      "name": "睡眠空间座椅设置入口",
      "query": "打开睡眠空间座椅设置",
      "verdict": "empty_required_slot",
      "operation_check": {
        "target_match": false,
        "action_match": true,
        "value_match": true,
        "evidence": "app:ctrl returned without a seat target"
      },
      "report": true
    }
  ]
}
```

For `pass`, all three `operation_check` booleans must be true. For reportable failures, `report` must be true. Controls on non-active pages are forbidden even when `report` is false; excluded pages belong only in `pages`.
