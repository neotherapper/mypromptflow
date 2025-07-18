# Stakeholder Questions for Maritime Insurance Platform

## 1. Quote Generation Strategy

**Decision Priority**: CRITICAL

**Context**: The B2C platform requires streamlined quote generation to compete effectively while balancing automation with flexibility.

**Questions**:

1. How should customers select coverage types in the quote process?
   • **Guided Selection**: AI-driven recommendations based on vessel and voyage data
   • **Full Choice**: Complete coverage menu with detailed explanations
   • **Tiered Options**: Basic/Standard/Premium packages with add-on flexibility

2. Should broker selection be integrated into the quote generation process?
   • **Transparent Choice**: Show all available brokers with rates and ratings
   • **Optimized Selection**: System recommends best broker per region automatically
   • **Hybrid Approach**: Best deal highlighted with option to compare alternatives

**Financial Impact**: Conversion rate differences of 15-30% between approaches. Guided selection reduces abandonment but may limit premium revenue. Full choice increases average quote value but decreases completion rates.

**Implementation Complexity**: Guided selection requires AI development (3-4 months). Full choice needs comprehensive UI/UX work (2-3 months). Tiered options require product structuring (1-2 months).

**Customer Experience**: Guided selection improves completion rates. Full choice increases perceived value. Tiered options simplify decision-making for non-experts.

**Competitive Risk**: Simplified approaches may appear less professional. Complex approaches may lose customers to competitors with faster processes.

**Business Impact**: Affects customer experience, conversion rates, and competitive differentiation in B2C maritime insurance market.

---

## 2. War Coverage Business Rules

**Decision Priority**: HIGH

**Context**: War coverage is a critical differentiator in maritime insurance. Strategic decisions on add-on coverage will impact pricing and market positioning.

**Questions**:

1. What are the rules for adding additional coverages when war coverage is selected?
   • **Always-Mandatory**: Automatically include War H&M, War LoH, and K&R with no deselection
   • **Suggested-Only**: System suggests add-ons but allows customer to deselect non-mandatory items
   • **Territory-Specific**: Admins maintain HRA-to-required-add-ons mapping table

2. How should coverage duration be determined?
   • **Standardized Periods**: Fixed options (7, 14, 30 days) per High Risk Area
   • **Customer Override**: Allow user-defined duration with premium adjustments
   • **Voyage-Based**: Duration tied to specific voyage requirements and routes

**Financial Impact**: Always-mandatory increases average policy value by 40-60% but may reduce conversion. Suggested-only maintains flexibility but risks coverage gaps. Territory-specific optimizes for regional requirements but increases operational complexity.

**Implementation Complexity**: Always-mandatory is simplest (1 month). Suggested-only requires advanced UI logic (2 months). Territory-specific needs admin tools and mapping system (3-4 months).

**Customer Experience**: Always-mandatory provides complete protection but reduces choice. Suggested-only offers flexibility but may confuse customers. Territory-specific appears most professional but complex.

**Regulatory Risk**: Always-mandatory ensures complete compliance. Suggested-only may create coverage gaps. Territory-specific requires ongoing regulatory monitoring.

**Competitive Advantage**: Comprehensive war coverage differentiation depends on mandatory approach. Flexibility may match competitors rather than exceed them.

**Business Impact**: Affects revenue capture, risk management, and competitive positioning in war risk coverage market.

---

## 3. Broker Partnership Model

**Decision Priority**: HIGH

**Context**: The broker relationship model must enhance B2C advantages while maintaining market access and competitive rates.

**Questions**:

1. How should broker relationships be structured in the platform?
   • **Broker-as-Customer**: Brokers use platform on behalf of ship owners
   • **Broker-as-Partner**: Independent brokers with platform integration
   • **Hybrid Model**: Both direct B2C and broker-mediated transactions

2. Should broker selection impact quote availability and pricing?
   • **Unique Rates**: Each broker has exclusive rates per region
   • **Standardized Pricing**: Consistent pricing across all brokers
   • **Competitive Bidding**: Brokers bid on individual quotes

**Financial Impact**: Broker-as-customer reduces direct revenue but increases volume. Broker-as-partner maintains margins but requires revenue sharing. Hybrid model maximizes reach but increases complexity costs.

**Implementation Complexity**: Broker-as-customer requires multi-tenant architecture (4-6 months). Broker-as-partner needs integration APIs (2-3 months). Hybrid model requires both systems (6-8 months).

**Customer Experience**: Broker-as-customer maintains familiar broker relationships. Broker-as-partner offers direct platform access. Hybrid model provides maximum choice but may confuse customers.

**Market Access**: Broker-as-customer leverages existing broker networks. Broker-as-partner requires new broker acquisition. Hybrid model maximizes market coverage but increases management complexity.

**Competitive Risk**: Broker-as-customer may commoditize platform. Broker-as-partner requires strong value proposition. Hybrid model prevents broker lock-in but increases competitive exposure.

**Business Impact**: Affects market reach, pricing strategy, and competitive position in B2C maritime insurance.

---

## 4. Quote Lifecycle Management

**Decision Priority**: MEDIUM

**Context**: The quote acceptance process must balance customer convenience with business risk management.

**Questions**:

1. How should quote expiration be managed?
   • **Universal SLA**: Common expiration timer for all customers
   • **Risk-Based Expiration**: Longer validity for lower-risk quotes
   • **Dynamic Pricing**: Prices adjust based on time remaining

2. What actions should occur at quote expiration?
   • **Automatic Renewal**: System revalidates and extends automatically
   • **Manual Reactivation**: Customer must request quote renewal
   • **Graduated Response**: Notifications escalate before expiration

**Financial Impact**: Universal SLA reduces operational costs but may lose high-value quotes. Risk-based expiration optimizes conversion but increases complexity. Dynamic pricing maximizes revenue but may confuse customers.

**Implementation Complexity**: Universal SLA is simplest (1 month). Risk-based expiration requires risk scoring integration (2-3 months). Dynamic pricing needs real-time pricing engine (4-5 months).

**Customer Experience**: Universal SLA provides predictability. Risk-based expiration appears tailored but may confuse customers. Dynamic pricing creates urgency but may reduce trust.

**Operational Efficiency**: Universal SLA minimizes support queries. Risk-based expiration requires manual oversight. Dynamic pricing needs continuous monitoring.

**Competitive Risk**: Universal SLA may lose quotes to competitors with longer validity. Risk-based expiration may appear arbitrary. Dynamic pricing may appear manipulative.

**Business Impact**: Affects customer experience, conversion rates, and operational efficiency.

---

## 5. Ship Broker Relationship Structure

**Decision Priority**: MEDIUM

**Context**: The B2C platform must accommodate ship brokers who manage multiple vessels on behalf of owners. The relationship structure affects user experience and business model scalability.

**Questions**:

1. How should ship broker vessel management be structured?
   • **Restricted Access**: Brokers limited to vessels they officially manage
   • **Verified Management**: Brokers prove management rights per vessel
   • **Owner Notification**: Ship owners notified of all broker activities

2. Should the platform support broker independence from ship owners?
   • **Owner-Dependent**: All broker actions require owner approval
   • **Independent Authority**: Brokers operate autonomously within limits
   • **Hybrid Authority**: Risk-based approval requirements

**Financial Impact**: Restricted access limits broker efficiency but reduces liability. Verified management increases onboarding costs but ensures authority. Owner notification increases operational costs but maintains transparency.

**Implementation Complexity**: Restricted access requires vessel-broker mapping system (2-3 months). Verified management needs document verification workflow (3-4 months). Owner notification requires multi-party communication system (2-3 months).

**Customer Experience**: Restricted access may frustrate efficient brokers. Verified management creates thorough but slow onboarding. Owner notification maintains trust but may create confusion.

**Legal Risk**: Restricted access minimizes unauthorized actions. Verified management provides audit trail. Owner notification reduces dispute potential but may create consent issues.

**Market Penetration**: Restricted access may limit broker adoption. Verified management appeals to professional brokers. Owner notification may slow broker acquisition.

**Business Impact**: Affects market penetration, user experience, and business model scalability.

---

## 6. Charterer Fleet Management

**Decision Priority**: MEDIUM

**Context**: The B2C platform must support charterers who operate vessels they don't own. This segment represents significant market opportunity but requires specific business model considerations.

**Questions**:

1. How should charterer fleet management be implemented?
   • **Charterer-Owned Fleet**: Charterers create and manage their own vessel database
   • **Integrated Fleet**: Combined owner/charterer vessel management system
   • **Reference-Only**: Charterers reference owner vessels without management rights

2. What information should be required from charterers?
   • **Charter Agreement**: Proof of charter rights and duration
   • **Vessel Authority**: Documentation of insurance authority
   • **Risk Assessment**: Charterer-specific risk factors and history

**Financial Impact**: Charterer-owned fleet increases market reach but requires duplicate data management. Integrated fleet optimizes efficiency but increases system complexity. Reference-only minimizes costs but limits charterer value.

**Implementation Complexity**: Charterer-owned fleet requires separate database architecture (3-4 months). Integrated fleet needs complex access controls (4-6 months). Reference-only requires basic linking system (1-2 months).

**Customer Experience**: Charterer-owned fleet provides full control but may duplicate effort. Integrated fleet offers seamless experience but may confuse ownership. Reference-only is simple but may feel limited.

**Data Quality**: Charterer-owned fleet risks data inconsistency. Integrated fleet maintains single source of truth. Reference-only depends on owner data quality.

**Market Opportunity**: Charterer-owned fleet maximizes charterer adoption. Integrated fleet appeals to sophisticated users. Reference-only may limit charterer engagement.

**Business Impact**: Affects market expansion, risk management, and operational complexity.

---

## 7. Extra Day Invoicing (Overstay Charges)

**Decision Priority**: HIGH

**Context**: When vessels remain in High-Risk Areas beyond covered periods, additional charges apply. This significantly impacts revenue and customer relationships.

**Questions**:

1. How should overstay charges be triggered?
   • **Automatic**: System detects via daily AIS monitoring
   • **Manual**: Triggered by admin request
   • **Hybrid**: Automatic detection with manual approval

2. Should overstay require new quote or use preset daily rates?
   • **New Quote**: Full underwriting for extended period
   • **Preset Rates**: Predetermined daily rates by risk zone
   • **Blended Approach**: Preset rates with manual review for high-risk extensions

3. Who should receive overstay invoices and notifications?
   • **Vessel Owner**: Direct billing to registered owner
   • **Policy Holder**: Billing to original policy purchaser
   • **Broker Mediated**: Notifications through broker relationships

**Financial Impact**: Automatic detection captures 95% of overstay revenue versus 60% manual. Preset rates improve cash flow but may under-price risk. New quotes optimize pricing but delay revenue collection.

**Implementation Complexity**: Automatic detection requires AIS integration (4-6 months). Manual triggering needs admin workflow (1-2 months). Hybrid approach requires both systems (5-7 months).

**Customer Experience**: Automatic detection provides immediate notification but may surprise customers. Manual triggering allows relationship management but delays response. Hybrid approach balances automation with human oversight.

**Revenue Risk**: Automatic detection minimizes revenue leakage. Manual triggering risks missed charges. Hybrid approach optimizes both revenue capture and customer relationships.

**Operational Efficiency**: Automatic detection reduces manual workload by 80%. Manual triggering requires dedicated resources. Hybrid approach balances automation with oversight needs.

**Business Impact**: Affects revenue capture, customer experience, and operational workload.

---

## 8. Sanctions Screening Process

**Decision Priority**: CRITICAL

**Context**: The screening process must balance compliance requirements with customer experience and processing speed. Regulatory violations carry severe penalties.

**Questions**:

1. What data sources should trigger sanctions screening?
   • **Static Lists**: Internally maintained country/port lists
   • **Live APIs**: Real-time sanctions feeds (OFAC, UN)
   • **Hybrid**: Combination of both approaches

2. When should sanctions questionnaires be presented?
   • **Inline**: During quote wizard if triggers detected
   • **Post-Submit**: After initial submission in blocking modal
   • **Pre-Screening**: Before quote process begins

3. What should happen to quotes flagged for sanctions review?
   • **Automatic Hold**: All flagged quotes require manual review
   • **Risk-Based**: Low-risk flags auto-approved, high-risk held
   • **Escalation Path**: Graduated review process based on risk level

**Financial Impact**: Static lists reduce API costs but risk false negatives. Live APIs increase operational costs but ensure current data. Hybrid approach balances cost with accuracy.

**Implementation Complexity**: Static lists require internal maintenance (2-3 months). Live APIs need integration infrastructure (3-4 months). Hybrid approach requires both systems (4-6 months).

**Customer Experience**: Inline screening provides immediate feedback but may interrupt flow. Post-submit screening maintains flow but may frustrate customers. Pre-screening eliminates surprises but adds friction.

**Regulatory Risk**: Static lists risk outdated information. Live APIs ensure current compliance. Hybrid approach provides redundancy and reduces regulatory exposure.

**Processing Speed**: Static lists enable fastest processing. Live APIs may cause delays. Hybrid approach balances speed with accuracy.

**Compliance Cost**: Manual review increases operational costs but ensures compliance. Risk-based processing optimizes resources but increases regulatory risk. Escalation paths balance efficiency with oversight.

**Business Impact**: Affects compliance, processing speed, and regulatory risk.

---

## 9. Financial & Reporting

**Decision Priority**: MEDIUM

**Context**: The system must generate financial reports for different stakeholder types while maintaining competitive advantage.

**Questions**:

1. Which stakeholder types should have access to financial reports?
   • **Ship Owners Only**: Restricted to vessel owners
   • **Charterers Only**: Limited to charterer activities
   • **Comprehensive Access**: Both ship owners and charterers with appropriate data

2. What level of financial detail should be provided?
   • **Summary Reports**: High-level financial overview
   • **Detailed Analytics**: Comprehensive financial breakdowns
   • **Customizable Reporting**: Stakeholder-specific report configuration

**Financial Impact**: Comprehensive reporting increases customer value but requires significant development investment. Summary reports minimize costs but may limit customer satisfaction. Customizable reporting maximizes value but increases complexity.

**Implementation Complexity**: Summary reports require basic dashboard development (2-3 months). Detailed analytics need comprehensive business intelligence system (4-6 months). Customizable reporting requires advanced configuration tools (6-8 months).

**Customer Experience**: Summary reports provide quick overview but may lack depth. Detailed analytics offer comprehensive insights but may overwhelm users. Customizable reporting provides personalized value but requires user configuration.

**Data Security**: Comprehensive access requires robust access controls. Restricted access simplifies security but may limit value. Customizable reporting needs granular permission system.

**Competitive Advantage**: Comprehensive reporting differentiates from competitors. Summary reports match industry standard. Customizable reporting creates unique value proposition.

**Business Impact**: Affects customer value proposition, data security, and competitive positioning.
