# DPIA Generation Skill - Romanian GDPR Compliance

## Skill Description

This skill enables Claude to generate comprehensive Data Protection Impact Assessments (DPIA / Evaluarea Impactului asupra Protecției Datelor) following the exact structure and methodology used by Romanian legal practitioners for GDPR compliance. The skill is specifically designed for Romanian legal and compliance contexts, following the template structure used by major Romanian organizations.

## Activation Triggers

Use this skill when:
- A user requests a DPIA (Evaluarea Impactului asupra Protecției Datelor) for data processing activities
- Analyzing data processing operations that may present high risks to data subjects' rights and freedoms
- Documenting legitimate interest assessments under Article 6(1)(f) GDPR
- The user mentions GDPR compliance documentation in Romanian legal context
- Creating employee monitoring or performance tracking documentation
- Assessing risks for new data processing systems or procedures

## Core DPIA Structure

### Document Metadata
- **Document title**: EVALUAREA IMPACTULUI ASUPRA PROTECȚIEI DATELOR
- **Activity/Process subject to DPIA**: Clear description of the processing activity
- **Detailed description of processing operations**: Comprehensive explanation of what data is being processed and how
- **Document version**: Format as X.0
- **Last update date and next review date**: DD.MM.YYYY format

### Main Sections (Roman Numerals)

#### I. DESCRIEREA ACTIVITĂȚII DE PRELUCRARE (art. 35 alin.(7) lit.(a) din GDPR)

**1. Scopurile și temeiurile aplicabile**
- Create a table with columns: Scopuri | Temeiuri juridice
- For each processing purpose, identify specific GDPR legal basis:
  - Art. 6 alin.1 lit. b) - contract performance
  - Art. 6 alin.1 lit. f) - legitimate interest
  - Art. 6 alin.1 lit. c) - legal obligation
- After the table, provide detailed explanation of each purpose with bullet points

**2. Categorii de persoane vizate**
- Identify all categories of data subjects (employees, customers, etc.)

**3. Modalitatea de informare**
- Reference Art. 13 and 14 GDPR
- Describe how data subjects will be informed (dedicated information notice)

**4. Categorii de date cu caracter personal**
Create a detailed table with columns:
- Categorii de date
- Caracterul general sau special al datelor
- Furnizarea datelor este obligatorie? (Da/Nu + legal basis if yes)
- Modalitatea de obținere (direct/indirect/prin observare/prin derivare)
- Scopul prelucrării (reference to question 1)

**5. Folosire pentru nou scop de prelucrare**
- State whether data is used only for declared purposes
- If new purposes exist, perform compatibility test

**6. Prelucrare pe "scară largă"**
Analyze based on four factors:
- i. Numărul persoanelor vizate
- ii. Volumul datelor și/sau diferitele tipuri de date
- iii. Durata sau permanența activităților
- iv. Aria geografică

**7. DEZVĂLUIRI ȘI TRANSFERURI DE DATE**
**Categorii de destinatari**
- List all recipients including processors (Art. 28 GDPR) and joint controllers (Art. 26 GDPR)
- Specify internal access (departments, roles)
- Reference data processing agreements

**8. Transfer în afara SEE**
- State if transfers outside EEA occur (Yes/No)

**9. Garanții de transfer**
- If transfers exist, specify safeguards (SCCs, BCRs, etc.)

**10. PROCESE DECIZIONALE AUTOMATIZATE**
- Describe extent of automated processing without human intervention
- Assess if decisions produce legal or similarly significant effects

#### II. NECESITATEA ȘI PROPORȚIONALITATEA ACTIVITĂȚII DE PRELUCRARE (art. 35 alin.(7) lit.(d) din GDPR)

**11. Obiectivul urmărit de Operator**
- For each processing activity/dashboard, explain:
  - The objective pursued
  - Why personal data processing is necessary
  - Rationale for any sensitive data processing

**12. Modalități alternative**
For each processing activity, analyze alternatives:
- **a) Approach without personal data** - explain and identify disadvantages
- **b) Pseudonymization** - explain benefits and limitations
- **c) Sample-based analysis** - explain when applicable and limitations
- Conclude why current approach is most effective

**13. Consimțământ** (if applicable)
- How consent validity is ensured
- How withdrawal mechanism works

**14. Reînnoire consimțământ** (if applicable)
- Mechanism for consent renewal

**15. Consecințe negative pentru Operator**
For each processing activity, list negative consequences if data is not processed:
- Operational inefficiencies
- Compliance risks
- Cost implications
- Service quality impacts
- Security vulnerabilities

**16. Consecințe pozitive**
Benefits for:
- **Operator**: Operational improvements, efficiency gains, cost savings
- **Terți/Societate**: Customer satisfaction, service quality, data security

#### III. ECHILIBRAREA INTERESULUI OPERATORULUI CU INTERESELE SAU DREPTURILE ȘI LIBERTĂȚILE PERSOANEI VIZATE

**17. AȘTEPTĂRI REZONABILE ȘI INTRUZIVITATE**
**Persoana vizată se așteaptă la prelucrare?**
- Analyze for each processing activity whether data subjects reasonably expect the processing
- Consider transparency, common practices, employment context

**18. Prelucrarea poate fi considerată intruzivă?**
For each activity, assess intrusion level:
- **Nivel de Intruzivitate**: Scăzut/Moderat/Ridicat
- Explain factors: monitoring extent, performance evaluation, continuous surveillance
- Provide mitigation measures:
  - a) Informare prealabilă (Art. 13 GDPR)
  - b) Minimizarea datelor și limitarea accesului
  - c) Securitatea datelor
  - d) Transparență și responsabilitate
  - e) Formare continuă și conștientizare

**19. Control de către persoana vizată**
- Explain how data subjects can control their data processing
- Reference information provided before collection
- Explain rights and how to exercise them

**20. CONSECINȚE PENTRU PERSOANA VIZATĂ**
**Consecințe negative**:
- Constant surveillance feelings
- Pressure and psychological stress
- Risk of disciplinary sanctions
- Privacy concerns
- Mitigation measures (access restrictions, periodic review, not daily monitoring)

**Consecințe pozitive**:
- Professional development opportunities
- Fair task distribution
- Performance recognition
- Training identification
- Improved service quality

#### IV. GARANȚIILE ȘI MĂSURILE IMPLEMENTATE

**22. Aplicații/sisteme IT folosite**
- List all IT systems and infrastructure used
- Reference Art. 28 GDPR agreements with processors
- Specify internal/external systems

**23. Măsuri tehnice și organizatorice**
Address each GDPR principle:

**Legalitate, echitate și transparență**:
- Legal basis identification and documentation
- Legitimate interest balancing
- Fairness through documented analysis
- Transparency through detailed information notices

**Limitări legate de scop**:
- Data used only for declared purposes

**Reducerea la minimum a datelor**:
- Only necessary data collected
- No Art. 9/10 GDPR special categories (unless specified)
- Access restricted based on need-to-know

**Exactitate/acuratețe**:
- Data obtained directly or through observation
- Accuracy maintenance procedures

**Limitări legate de stocare**:
- Limited retention periods
- Deletion/destruction procedures
- Timeline for establishing retention periods

**Integritate și confidențialitate**:
- Internal policies on access and use
- Technical security measures
- Periodic audits
- Penetration testing
- Contractual provisions with partners
- Periodic training programs

**Responsabilitate**:
- Documentation of processing activities
- Risk assessment and mitigation
- Information notice preparation
- Processing register updates
- Adoption of necessary documentation

**24. Protecția datelor încă de la concepere și implicit**
- Technical and organizational measures from design phase
- Data minimization at design level
- Purpose limitation measures
- Appropriate safeguards for data subjects
- Short storage periods
- Access and use limitations
- Compliance with DPIA measures

**25. Măsuri pentru protejarea drepturilor persoanei vizate**
- Contact information for Data Protection Officer (DPO)
- Mechanisms for exercising rights

**26. Alte măsuri organizatorice sau tehnice**
- Reference Section V measures

#### V. ANALIZA RISCURILOR AFERENTE PRELUCRĂRII

Create comprehensive risk table with columns:
1. **Riscuri pentru persoanele vizate** - Describe risk and source
2. **Severitate** - Scăzută/Medie/Mare
3. **Probabilitate** - Scăzută/Medie/Mare
4. **Evaluarea riscului inițial** - Scăzut/Mediu/Ridicat (based on matrix)
5. **Măsuri preconizate** - Detail mitigation measures with:
   - Responsible party
   - Timeline (in days/months from analysis date)
6. **Risc rezidual** - Scăzut/Scăzută
7. **Status** - De implementat/Implementat

**Standard risks to include**:
1. Lipsa informării corespunzătoare/Neconformarea cu transparența
2. Lipsa unui temei valabil/Prevalența drepturilor persoanelor vizate/Nerespectarea minimizării
3. Prelucrarea pentru durată mai mare/Neconformarea cu limitarea stocării
4. Lipsa unor măsuri de securitate/Neconformarea cu integritatea și confidențialitatea
5. Necompletarea Evidenței Prelucrărilor
6. Neactualizarea DPIA

#### VI. NECESITATEA CONSULTĂRII CU FACTORI INTERESAȚI

**27. Consultarea reprezentanților persoanelor vizate**
- State whether consultation occurred
- Justify decision (usually: standard processing, no high residual risk after DPIA)

#### VII. Aprobarea și Avizul DPIA

**Aprobarea**:
- Manager name and title
- Executive Director name and title
- Signature lines

**Aviz**:
- DPO confirmation statement
- Date and signature line

### Anexa Explicativă - Risk Assessment Matrix

Include visual matrix showing:
- Probabilitate axis (Scăzută/Medie/Mare)
- Severitate axis (Scăzută/Medie/Mare)
- Risk levels: Scăzut (green)/Mediu (yellow)/Ridicat (red)

## Key Principles for Generation

### Language and Terminology
- **Always use Romanian language** for DPIA documents
- Use proper GDPR article references: "Art. 6 alin.1 lit. f) din GDPR"
- Reference Romanian law when applicable: "Legea nr. 190/2018"
- Use formal legal terminology appropriate for Romanian legal practice

### Structure Requirements
- Use Roman numerals for main sections (I, II, III, IV, V, VI, VII)
- Use Arabic numerals for questions (1, 2, 3, etc.)
- Use bullet points sparingly - prefer numbered lists or paragraph format for detailed analysis
- Create tables where specified in the template

### Analysis Depth
- Provide thorough analysis for each processing activity
- Consider multiple alternatives in section II.12
- Assess intrusion levels honestly and comprehensively
- Balance operator interests with data subject rights
- Include both negative and positive consequences

### Risk Assessment
- Use the three-level scale: Scăzută/Medie/Mare
- Apply matrix methodology for initial risk evaluation
- Ensure residual risk is Scăzut after mitigation measures
- Specify concrete responsibilities and timelines
- Include standard compliance risks (information, legal basis, retention, security, register, DPIA updates)

### Practical Considerations
- Reference Art. 28 GDPR agreements with processors
- Reference Art. 26 GDPR agreements with joint controllers
- Include DPO contact information
- Specify information notice requirements
- Address employee monitoring concerns appropriately
- Consider Romanian workplace context

### Common Processing Activities to Address
- Employee performance monitoring dashboards
- Customer service call center operations
- License management systems
- Fraud prevention systems
- Analytics tools usage
- Productivity tracking systems

### Mitigation Measures Framework
When suggesting measures, always include:
- Prior information to data subjects
- Data minimization and access limitation
- Data security measures
- Transparency and accountability
- Continuous training and awareness
- Periodic (not daily) review schedules
- Need-to-know access restrictions
- Documented procedures for data use

## Output Format

Generate the DPIA as a comprehensive document with:
- Clear section headers using proper Romanian formatting
- Tables where specified
- Detailed analysis for each question
- Concrete, actionable mitigation measures
- Professional tone appropriate for submission to authorities
- Complete risk assessment with matrix
- Signature sections for approval

## Critical Reminders

1. **Never skip sections** - every numbered question must be addressed
2. **Provide specific legal basis** - don't use generic references
3. **Balance is key** - acknowledge both benefits and risks
4. **Mitigation must be concrete** - specify who, what, when
5. **Residual risk should be low** - if not, reconsider processing or add measures
6. **Romanian context matters** - consider ANSPDCP practice and Romanian employment law
7. **DPO involvement** - always reference DPO review and approval
8. **Processing register** - always include measure to update the register
9. **Information notice** - always include measure to create/update information notice
10. **Review period** - typically specify DPIA review every 3 years or when changes occur

## Example Phrases and Formulations

### Legal Basis Statements
- "Art. 6 alin.1 lit. b) din GDPR, respectiv executarea contractului individual de muncă"
- "Art. 6 alin.1 lit. f) din GDPR, respectiv interesul legitim al operatorului de a..."

### Information Statements
- "În conformitate cu art. 13 și 14 din GDPR, persoanele vizate trebuie să fie informate direct..."
- "Angajații vor fi informați cu privire la prelucrarea datelor lor prin intermediul unei Note de informare dedicate"

### Risk Mitigation
- "Responsabil: [Department/Role]"
- "Termen: În termen de 30 de zile de la data prezentei analize"
- "Măsură preconizată: [Specific action]"

### Conclusions
- "În concluzie, [summary of analysis]"
- "Pe baza acestor informații, se poate argumenta că..."
- "Prin urmare, utilizarea datelor cu caracter personal... pare să fie cea mai eficientă metodă..."

---

This skill enables precise generation of Romanian GDPR-compliant DPIAs following established legal practice in Romania, particularly for employment and customer service contexts.
