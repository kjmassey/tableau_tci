# Publishing Workbooks & Datasources
---
The ability to publish workbooks and datasources is a powerful capability of both the REST API and TSC. These methods - and others, such as downloading an item - can be used to automate moving items from one project/site/environment. For example, where I work, we use the TSC to move items from pre-production to production environments after the user has obtained the required approval(s). Since only an extremely limited number of users can publish to production, without automation our SLAs for completing these requests was very high (five bus. days), not to mention a constant dissatisfier! The vast majority of our deployments now completely within 15-30 mins of approval.

*There are fundamental differences in how the REST API and TSC handle file uploads - especially files >64MB. Basic examples will be given for both approaches, but using TSC is **highly** recommended when possible.*

*For simplicity and clarity, examples will **not** be provided for REST API + TWBX/TDSX files -- see Tableau's documentation*

---
We'll cover the following in this module:

#### - Publishing a workbook
#### - Publish a datasource
#### - Dealing with credentials, connection updates

---

*Open the REST API and TSC examples side-by-side for easier comparison, if your screen allows*
