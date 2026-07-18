# Comprehensive End-to-End Industry Use Cases

*The following use cases are designed to be universally compatible with any full-stack, API, or AI-centric prompt template. Copy the text block of the desired industry and paste it into the `[INSERT YOUR SPECIFIC USE CASE HERE]` placeholder of your chosen architecture prompt.*

***

### 1. Healthcare
An Intelligent Patient Care & Diagnostic Triage Platform. The system must serve two distinct user roles: Patients and Medical Professionals. 
1. **Core Functionality:** Patients must be able to securely register, book appointments, and view their lab results. Medical Professionals need a secure dashboard to manage patient electronic health records (EHR), update clinical notes, and manage hospital schedules.
2. **Intelligent Triage & Analytics:** The system must feature a specialized module that analyzes incoming patient symptoms alongside their historical clinical notes to automatically categorize the urgency of the case. It should summarize complex lab results into easily readable formats for the patient, and draft suggested follow-up care plans for the physician's final review. 
3. **Compliance & Security:** All data handling must strictly simulate HIPAA compliance requirements, ensuring robust role-based access control (RBAC), secure data storage, and comprehensive immutable audit logging for every time a medical record is accessed or modified.

### 2. BFSI (Banking, Financial Services, and Insurance)
A Secure Digital Banking & Automated Risk Assessment Portal. The system must serve Retail Customers and Bank Administrators.
1. **Core Functionality:** Customers must be able to view account balances, transfer funds securely, and submit loan/credit applications. Administrators and Loan Officers need a portal to review applications, manage user accounts, and track branch liquidity.
2. **Intelligent Analytics:** Implement an automated fraud detection mechanism that analyzes transaction patterns in real-time to flag anomalies. Additionally, build an automated loan risk scoring engine that evaluates applicant financial history to suggest approval, denial, or manual review.
3. **Compliance & Security:** The system must enforce strict KYC (Know Your Customer) data tracking, simulate PCI-DSS security standards for transactional data, and implement Multi-Factor Authentication (MFA) and immutable ledger logging for all financial movements.

### 3. Manufacturing
A Smart Factory Floor & Predictive Maintenance System. The system must serve Floor Operators and Plant Managers.
1. **Core Functionality:** Floor Operators need an interface to log machine usage, report defects, and view daily production quotas. Plant Managers require a macro-dashboard tracking overall factory output, raw material inventory levels, and shift scheduling.
2. **Intelligent Analytics:** Implement a predictive maintenance engine designed to analyze simulated IoT sensor data (e.g., machine vibration, temperature, operating hours) to predict equipment failures before they happen, automatically generating and assigning maintenance tickets to technicians.
3. **Compliance & Security:** The system must track ISO quality standard compliance, log worker safety incidents for OSHA reporting, and ensure high-availability operational uptime.

### 4. Retail & E-Commerce
A Next-Generation E-Commerce Storefront & Intelligent Inventory Manager. The system must serve Shoppers and Store Administrators/Vendors.
1. **Core Functionality:** Shoppers require a responsive storefront with a searchable product catalog, dynamic shopping cart, and secure checkout flow. Administrators need a backend portal for managing product listings, tracking order fulfillment, and managing customer returns.
2. **Intelligent Analytics:** Implement a personalized product recommendation engine that analyzes a user's browsing history and cart data to suggest complementary items. Additionally, build a dynamic pricing or low-stock alert module that notifies admins when inventory forecasting predicts a stockout.
3. **Compliance & Security:** Enforce strict GDPR/CCPA compliant user data handling, secure integration points for third-party payment gateways, and robust session management to prevent cart hijacking.

### 5. SCM (Supply Chain Management)
A Global Logistics Tracking & Automated Route Optimization Hub. The system must serve Dispatchers and Fleet Drivers/Vendors.
1. **Core Functionality:** Dispatchers need a centralized dashboard to track shipment statuses from warehouse to final delivery, manage purchase orders, and monitor vendor invoices. Drivers need a mobile-friendly interface to update delivery statuses and log proof of delivery.
2. **Intelligent Analytics:** Implement a logistics engine that forecasts seasonal inventory demand to trigger automated reorder alerts. Include a simulated route optimization module that calculates the most efficient delivery paths based on variables like distance, priority, and simulated traffic.
3. **Compliance & Security:** Track international trade compliance documents, monitor supplier SLA (Service Level Agreement) performance, and ensure secure, authenticated API access for external vendor integrations.

### 6. IT (Information Technology)
An Intelligent IT Service Desk & Asset Management Platform. The system must serve internal Employees and IT Support Staff.
1. **Core Functionality:** Employees need a self-service portal to submit support tickets, request hardware, and view the status of their requests. IT Staff require a dashboard to claim, update, and resolve tickets, as well as track company assets (laptops, software licenses).
2. **Intelligent Analytics:** Implement an automated ticket triaging system that uses Natural Language Processing to read issue descriptions, categorize them (e.g., Networking, Hardware, Security), and route them to the correct department. Include a knowledge-base semantic search feature that suggests solutions to employees before they submit a ticket.
3. **Compliance & Security:** Enforce strict SOC2 compliance auditing, track SLA resolution times, and implement strict RBAC so only authorized admins can access sensitive infrastructure requests.

### 7. Hospitality (Hotel or Restaurant)
A Dynamic Hospitality Reservation & Guest Experience Management System. The system must serve Guests and Hotel/Restaurant Staff.
1. **Core Functionality:** Guests need a seamless booking portal to reserve rooms or tables, modify reservations, and view amenities. Staff require an operational dashboard for room/table assignment, housekeeping/kitchen scheduling, and billing management.
2. **Intelligent Analytics:** Implement a dynamic pricing engine that adjusts room or table booking rates based on simulated local events, historical occupancy data, and seasonal demand. Include an automated guest feedback analyzer that runs sentiment analysis on reviews to immediately flag negative experiences to management.
3. **Compliance & Security:** Ensure secure handling of guest PII (Personally Identifiable Information), simulated secure POS (Point of Sale) integration, and strict data retention policies.

### 8. Sales and Marketing
An AI-Enhanced CRM & Marketing Campaign Orchestrator. The system must serve Sales Representatives and Marketing Managers.
1. **Core Functionality:** Sales Reps need a pipeline dashboard to track leads, log customer interactions, and manage deal stages. Marketing Managers require tools to create email campaigns, define audience segments, and track click-through metrics.
2. **Intelligent Analytics:** Implement a lead scoring algorithm that analyzes customer engagement data (e.g., website visits, email opens) to identify high-conversion prospects and automatically alert sales reps. Include a generative module that drafts personalized follow-up email copy based on the lead's industry and previous interactions.
3. **Compliance & Security:** Strictly enforce CAN-SPAM and GDPR compliance for all marketing communications, manage user opt-out lists robustly, and ensure sales data is siloed appropriately by region or team.

### 9. Social Media
A Highly Scalable Social Networking & Content Moderation Platform. The system must serve Standard Users and Platform Moderators.
1. **Core Functionality:** Users need the ability to create profiles, post content (text/media), follow others, and interact via likes and comments in real-time. Moderators require an administrative dashboard to review flagged content, suspend accounts, and manage community guidelines.
2. **Intelligent Analytics:** Implement an algorithmic content feed that prioritizes highly engaging posts tailored to individual user preferences. Build an automated content moderation engine that analyzes text to detect toxic behavior, hate speech, or spam, automatically flagging or hiding severe violations for human review.
3. **Compliance & Security:** Enforce digital copyright compliance (DMCA takedown processes), strict user privacy and data-sharing controls, and robust rate-limiting to prevent bot spam.

### 10. Education
An Adaptive Learning Management System (LMS) & Student Analytics Portal. The system must serve Students and Educators.
1. **Core Functionality:** Students require a portal to access course materials, submit assignments, and view grades. Educators need an interface to manage curriculum content, grade submissions, and track classroom attendance.
2. **Intelligent Analytics:** Implement an adaptive learning module that analyzes a student's quiz scores to identify weak areas and automatically recommends specific supplementary study materials. Include an AI-assisted grading tool that can evaluate short-form answers or check essays for semantic similarity to existing sources (plagiarism detection).
3. **Compliance & Security:** Ensure strict compliance with FERPA (Family Educational Rights and Privacy Act) for student data protection, and implement web accessibility standards (WCAG) so the platform is usable by students with disabilities.

### 11. Sports and Athletics
A Comprehensive Team Management & Player Performance Analytics Platform. The system must serve Athletes, Coaches, and Team Managers.
1. **Core Functionality:** Athletes need a mobile-friendly portal to view upcoming training schedules, log their daily wellness metrics (sleep, nutrition, soreness), and watch match replays. Coaches and Managers require a centralized dashboard to design training programs, manage roster availability, and track overall team statistics across seasons.
2. **Intelligent Analytics:** Implement a player performance engine that analyzes historical match data and daily wellness logs to calculate injury risk probabilities, automatically alerting coaches to rest specific players. Include a computer vision or statistical module that analyzes match event data to generate automated post-game tactical summaries and highlight clips for video review.
3. **Compliance & Security:** Ensure strict data privacy compliance for athlete medical and wellness data, secure integration with wearable APIs (e.g., GPS trackers, heart rate monitors), and robust role-based access so tactical data is siloed from rival teams.

### 12. Transportation & Mobility
A Next-Generation Fleet Management & Smart Dispatch Platform. The system must serve Fleet Operators, Drivers, and Corporate Clients.
1. **Core Functionality:** Drivers require a mobile application to view dispatched routes, log hours of service (HOS), and perform daily vehicle inspection reports. Corporate Clients need a booking portal to request transport services and track their cargo/passengers. Fleet Operators require a centralized command center dashboard to assign vehicles, track real-time GPS locations, and manage fleet maintenance schedules.
2. **Intelligent Analytics:** Implement a dynamic dispatch engine that automatically assigns the nearest, properly-equipped vehicle to a new request based on real-time driver availability and traffic conditions. Include a fuel optimization module that analyzes historical route data and driving behaviors (e.g., harsh braking, idling) to generate coaching alerts and reduce overall fleet fuel consumption.
3. **Compliance & Security:** Enforce strict Electronic Logging Device (ELD) mandate compliance for driver hours, ensure robust data encryption for GPS tracking to prevent location spoofing, and implement strict RBAC so clients can only view their specific assigned vehicles.
