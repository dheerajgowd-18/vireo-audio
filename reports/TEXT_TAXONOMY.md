# Support Ticket Text Taxonomy Specification

**Version:** 1.0.0  
**Effective Date:** 2026-09-30  
**Scope:** Vireo Audio Customer Support Inbound Messages and Agent Closing Notes  

---

## 1. Issue Category Taxonomy

The issue taxonomy defines 9 distinct operational categories derived directly from an empirical audit of 11,750 customer messages across chat, email, voice (IVR), and social channels.

| Category Label | Definition | Inclusion Examples | Exclusion Examples | Business & Operational Rationale |
| :--- | :--- | :--- | :--- | :--- |
| `delivery_shipping` | Inquiries and complaints regarding transit logistics, tracking delays, courier non-delivery, or package damage during transit. | • *"my order has not been delivered yet"*<br>• *"order not delivered, tracking not updating"*<br>• *"courier marked delivered but nobody got anything"* | • Return pickup courier delays (classify under `returns_refunds`).<br>• Damaged product internals without box damage (classify under `hardware_audio_defect`). | High logistics transfer volume (1,907 tickets); critical for monitoring 3PL delivery SLA and transit insurance claims. |
| `returns_refunds` | Queries and requests regarding return eligibility, pickup scheduling, QC inspection status, or refund timeline. | • *"still waiting for my refund"*<br>• *"nobody came for the pickup"*<br>• *"return received but refund not processed"* | • Pre-dispatch cancellation requests (classify under `cancellation`).<br>• Goodwill store credit inquiries (classify under `billing_payment`). | Governed by Policy §5 return window; directly drives cash outflows and return logistics costs (₹340/pickup). |
| `billing_payment` | Inquiries regarding duplicate payment deductions, failed gateway checkouts, GST invoice requests, or promotional coupon failures. | • *"paid via UPI, amount deducted, no order"*<br>• *"card charged two times"*<br>• *"invoice not downloading, need GST bill"* | • Refund status after a physical return (classify under `returns_refunds`). | Billing issues generate high customer anxiety; fast first response prevents credit card chargebacks and payment gateway disputes. |
| `charging_battery` | Specific customer reports of battery degradation, charging case failures, or earbud charging contact pin defects. | • *"the left earbud is not charging at all"*<br>• *"one of them never gets green light in case"*<br>• *"battery life has dropped to almost nothing"* | • General Bluetooth dropouts while battery is charged (classify under `connectivity_pairing`). | Critical signature for the Pulse 2 manufacturing lot crisis; separates power-rail failure from wireless protocol issues. |
| `connectivity_pairing` | Issues establishing or maintaining Bluetooth pairing, wireless connection drops, or mobile companion app discovery failures. | • *"bluetooth keeps cutting out"*<br>• *"phone just doesn't see it in the list anymore"*<br>• *"pairing is not working with laptop"* | • Device fails to turn on due to depleted battery (classify under `charging_battery`). | Solvable via frontline agent troubleshooting resets without issuing expensive physical hardware replacements. |
| `hardware_audio_defect` | Physical audio driver degradation, crackling/distortion, microphone failure, or unilateral speaker failure unrelated to battery. | • *"no sound from the right earbud"*<br>• *"severe distortion at high volume"*<br>• *"mic is muffled on phone calls"* | • Earbud is completely dead and uncharged (classify under `charging_battery`). | Governed by Policy §6 Escalations & Warranty (Tier 2); requires certified hardware inspection and RMA approval. |
| `cancellation` | Explicit customer requests to cancel an order prior to warehouse dispatch or fulfillment. | • *"cancel order VR896827"*<br>• *"ordered wrong color, please cancel"*<br>• *"cancel order immediately"* | • Post-delivery return requests (classify under `returns_refunds`). | Fast identification stops warehouse shipment before dispatch, saving reverse logistics costs (₹340) and re-handling fees. |
| `product_enquiry_setup` | Pre-purchase questions, feature specifications, firmware setup walkthroughs, or device compatibility questions. | • *"does the AirLite work with iPhone?"*<br>• *"how to update firmware to latest version?"*<br>• *"is Strata 3 waterproof?"* | • Technical malfunction during normal usage (classify under `connectivity_pairing` or `charging_battery`). | Tier 1 frontline first-contact resolution opportunity; deflection potential via self-service FAQ and automated bot responses. |
| `other_unclear` | Ambiguous complaints, fragmented/unintelligible customer text, greetings without intent, or test messages. | • *"urgent pls call me"*<br>• *"hello hello"*<br>• *"..."* | • Actionable issues with typo (e.g. *"cancle ordr"* should be mapped to `cancellation`). | Isolates unusable input; prevents noise from polluting operational categories. |

---

## 2. Resolution Outcome Taxonomy

The resolution outcome taxonomy classifies the action taken by the resolving support agent based on `agent_notes` and policy actions.

| Outcome Label | Definition | Inclusion Evidence (Agent Notes & Policy) | Operational Relevance |
| :--- | :--- | :--- | :--- |
| `replacement_approved` | An RMA was created, and a replacement device was authorized or dispatched. | Notes: *"replacement approved"*, *"rplc raised"*, *"rma shared"*, *"new unit shipped"*. Ticket: `replacement_issued == 'Y'`. | Directly incurs unit cost + ₹340 logistics cost (Policy §5); must be monitored for Tier 1 vs Tier 2 compliance. |
| `refund_processed` | A monetary refund was initiated to the customer's original payment method or UPI. | Notes: *"refund initiated"*, *"full refund processed"*, *"reversal logged"*. Ticket: `refund_amount_inr > 0`. | Direct cash outflow; governed by Policy §5 reason codes and anti-dual benefit rules. |
| `troubleshooting_resolved` | Customer walked through device reset, charging contact cleaning, or pairing reset successfully. | Notes: *"walked through forget + re-pair"*, *"cleaned contacts, working now"*, *"re-pair successful"*. | Represents true first-contact resolution without inventory loss; optimal operational target. |
| `courier_escalated` | Ticket escalated to 3PL logistics partner for delivery address update, AWB tracing, or transit claim. | Notes: *"checked with courier partner"*, *"raised ticket with logistics"*, *"re-raised pickup w/ crr"*. | Measures external delivery partner friction and re-handling overhead. |
| `store_credit_issued` | Customer was granted store credit due to first-response SLA breach (₹350) or Team Lead approved goodwill. | Notes: *"store credit issued"*, *"sla credit added"*, *"goodwill credit approved"*. | Direct P&L charge to support SLA credit line (Policy §3). |
| `unresolved_ambiguous` | Agent notes contain uninformative shorthand or administrative closure without explicit resolution details. | Notes: *"see prev"*, *"- [closed]"*, *"sorted"*, *"cx ok"*, *"closed"*. | Identifies agent documentation quality gaps and training needs. |
