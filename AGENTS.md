# Security Audit & Secure Coding Rules

Before generating or modifying code touching authentication, authorization, database queries, API routes, file uploads, or external integrations, apply these checks:

1. **OWASP & Logic Review (Cloudflare Security Audit)**
   - Enforce server-side authorization checks on every endpoint and resource lookup (prevent IDOR/BOLA).
   - Use parameterized queries or ORM bindings exclusively; never concatenate raw user input into SQL, shell commands, or templates.
   - Validate and sanitize all request payloads, headers, and file uploads at the boundary.

2. **Secrets & Least Privilege**
   - Never hardcode API keys, tokens, database URLs, or credentials. Reference environment variables only.
   - Scope IAM roles, OAuth tokens, and database permissions to the minimum required privileges.