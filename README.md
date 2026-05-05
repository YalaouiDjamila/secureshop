# SecureShop – Intentionally Vulnerable Microservices Platform

> **Workshop 3 – DevSecOps Security Assessment Lab**  
> **SecureShop** is an intentionally vulnerable e-commerce microservices platform built for educational purposes to demonstrate a complete **DevSecOps pipeline** in a controlled lab environment.

---

## Disclaimer

> **This project is intentionally vulnerable and must never be deployed in production.**

All vulnerabilities in this repository were **manually introduced for educational purposes** to demonstrate how modern DevSecOps security tools detect weaknesses across the software development lifecycle.

This project is part of an academic security workshop and exists solely for:

- learning secure development practices,
- understanding DevSecOps tooling,
- simulating real-world vulnerabilities in a safe environment,
- practicing detection, reporting, and remediation workflows.

---

## Project Overview

SecureShop is a lightweight **e-commerce microservices platform** composed of multiple independent services communicating through an API Gateway.

The project was designed to simulate a realistic cloud-native application while intentionally embedding vulnerabilities in:

- source code,
- dependencies,
- container images,
- infrastructure configuration,
- runtime secrets,
- CI/CD pipelines.

Its purpose is to provide a full-stack environment for applying and evaluating **DevSecOps practices**.

---

## Objectives

This project demonstrates how to:

- apply **DevSecOps principles** across the SDLC,
- integrate security into CI/CD pipelines,
- detect vulnerabilities using automated security tools,
- correlate findings with threat models,
- manage secrets securely at runtime,
- assess security across code, containers, dependencies, and infrastructure.

---

## Architecture Overview

SecureShop follows a **microservices architecture** with six backend services and one API Gateway.

### Microservices

| Service | Port | Responsibility |
|--------|------|----------------|
| User Service | 8001 | Registration, login, JWT issuance, profile management |
| Product Service | 8002 | Product catalogue, search, categories |
| Order Service | 8003 | Cart management, order lifecycle |
| Payment Service | 8004 | Payment initiation, transaction records |
| Notification Service | 8005 | Email/SMS dispatch |
| Inventory Service | 8006 | Stock management and reservation |

### Gateway

An **Nginx API Gateway** acts as the single entry point for all external traffic and provides:

- request routing,
- rate limiting,
- TLS termination,
- authentication forwarding,
- centralized exposure control.

---

## Threat Modeling

Threat modeling was performed before implementation using:

- **DFD Level 0**
- **DFD Level 1**
- **STRIDE Analysis**

### Key Threats Identified

- **Spoofing** → weak JWT secret, credential theft
- **Tampering** → unsafe deserialization, command injection
- **Repudiation** → lack of structured audit logs
- **Information Disclosure** → hardcoded secrets, version leakage
- **Denial of Service** → vulnerable dependencies, malformed inputs
- **Elevation of Privilege** → root containers, shell injection

---

## Repository Structure

```bash
secureshop/
├── .env.example
├── .gitignore
├── .gitleaks.toml
├── pom.xml
├── README.md
├── .github/
│   └── workflows/
│       └── devsecops.yml
├── docs/
│   ├── findings.md
│   ├── security-report.md
│   └── stride-analysis.md
├── gateway/
│   ├── Dockerfile
│   └── nginx.conf
├── infrastructure/
│   ├── docker-compose.yml
│   └── vault-init.sh
├── services/
│   ├── user-service/
│   ├── product-service/
│   ├── order-service/
│   ├── payment-service/
│   ├── notification-service/
│   ├── inventory-service/
│   └── java-service/
└── target/
```

---

## DevSecOps Toolchain

| Category | Tool | Purpose |
|---------|------|---------|
| SAST | Bandit | Python static security analysis |
| SAST | Semgrep | Multi-language static analysis |
| SAST | CodeQL | Deep semantic code analysis |
| SCA | Trivy (fs) | Dependency vulnerability scanning |
| SCA | OWASP Dependency-Check | CVE detection in dependencies |
| Secrets | Gitleaks | Hardcoded secret detection |
| Containers | Trivy (image) | Container image vulnerability scanning |
| DAST | OWASP ZAP | Runtime web security testing |
| IaC | Checkov | Infrastructure misconfiguration scanning |
| IaC | Hadolint | Dockerfile linting |
| Runtime Secrets | HashiCorp Vault | Secure secrets management |
| SBOM | Syft | Software Bill of Materials generation |
| Reporting | GitHub Security Tab | SARIF aggregation and reporting |

---

## Security Assessment Scope

- **Step 0** – Threat Modeling  
- **Step 1** – Project Setup  
- **Step 2** – SAST Analysis  
- **Step 3** – SCA Analysis  
- **Step 4** – Secrets Detection  
- **Step 5** – Container Image Scanning  
- **Step 6** – DAST Analysis  
- **Step 7** – Infrastructure-as-Code Security  
- **Step 8** – Runtime Secrets Management  
- **Step 9** – CI/CD Pipeline Security  
- **Step 10** – Security Dashboard & Reporting  

---

## Key Findings

### Examples of Injected Vulnerabilities

- OS Command Injection (`shell=True`)
- MD5 Password Hashing
- SQL Injection
- Unsafe Pickle Deserialization
- XXE Injection
- Hardcoded Secrets
- Log4Shell (`CVE-2021-44228`)
- Vulnerable Python dependencies
- Insecure Dockerfiles
- Missing Security Headers
- Root Containers
- Secrets baked into container images

### Findings Summary

| Category | Total Findings |
|---------|----------------|
| SAST | 16 |
| SCA | 20 |
| Secret Scanning | 29 |
| Container Scanning | 363 |
| DAST | 5 |
| IaC | 13 |
| **Total** | **446** |

---

## CI/CD Pipeline

The project includes a full **GitHub Actions DevSecOps pipeline** defined in:

```bash
.github/workflows/devsecops.yml
```

### Pipeline Stages

- SBOM generation
- SAST scanning
- SCA scanning
- Secret scanning
- Vault secrets validation
- Container image scanning
- IaC security checks
- Docker linting
- DAST scanning
- SARIF upload to GitHub Security

---

## Runtime Secrets Management

To demonstrate secure secret handling, SecureShop integrates **HashiCorp Vault** in development mode.

---

## Running the Project

### Prerequisites

- Docker
- Docker Compose
- Python 3.11+
- Java 17+
- Git

### Start the Lab Environment

```bash
docker compose -f infrastructure/docker-compose.yml up --build
```

---

## Authors

- **YALAOUI Djamila**
- **LAKEHAL Amani Ala**
