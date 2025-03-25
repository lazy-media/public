# Authentik Applications & Providers Setup Guide

## Section 1: Proxy Provider Setup

### Method 1: Easy Wizard Setup

1. **Login** to your Authentik Admin Account
2. Navigate to `Applications > Applications`
   - Click `Create with Wizard`
   - Enter application details:
     - Name (e.g., "Sonarr")
     - Slug (autofilled or manual)
     - (Optional) Group name (e.g., "Admins", "Nextcloud Users")
       - Note: Group names must be exact matches
   - (Optional) Configure UI Settings:
     - Launch URL (use `blank://blank` to hide app)
     - Enable `Open in new tab`
   - Click `Next`
3. Select `Transparent Reverse Proxy` → `Next`
4. Configure provider settings:
   - Provider name (usually autofilled)
   - (Optional) Authentication Flow
   - Authorization Flow:
     - Implicit: No confirmation dialog
     - Explicit: Shows confirmation dialog
5. Enter host details:
   - External Host: FQDN (e.g., `https://test.domain.example`)
   - Internal Host: Service IP:Port (e.g., `http://192.168.1.10:8080`)
     - Important: Disable SSL validation for HTTPS internal hosts
6. Expand `Advanced Protocol Settings`:
   - Select your Cloudflare Certificate
   - (Optional) Add `/` to `Unauthenticated Paths` for testing
7. Complete setup:
   - Click `Next` or `Finish`
   - Navigate to `Applications > Outposts`
   - Edit `authentik Embedded Outpost`
     - Move application to right column
   - Click `Update`

### Method 2: Manual Setup

1. **Create Provider**:
   - Navigate to `Applications > Providers` → `Create`
   - Select `Proxy Provider` → `Next`
   - Configure:
     - Name
     - (Optional) Authentication Flow
     - Authorization Flow (Implicit/Explicit)
     - Select `Proxy` mode
     - External Host (FQDN)
     - Internal Host (IP:Port)
       - Disable SSL validation for HTTPS internal hosts
     - Advanced Settings:
       - Select Cloudflare Certificate
       - (Optional) Add `/` to `Unauthenticated Paths`
   - Click `Finish`

2. **Create Application**:
   - Navigate to `Applications > Applications` → `Create`
   - Configure:
     - Name and slug
     - (Optional) Group name
     - Select provider
     - (Optional) UI Settings:
       - Launch URL (`blank://blank` to hide)
       - `Open in new tab`
       - Upload icon
   - Click `Create`

3. **Configure Outpost**:
   - Navigate to `Applications > Outposts`
   - Edit `authentik Embedded Outpost`
     - Move application to right column
   - Click `Update`

## Section 2: OAuth2/OpenID Setup

### Using Easy Setup Wizard

1. Navigate to `Applications > Applications` → `Create with Wizard`
2. Enter basic info:
   - Name (e.g., "Example OAuth")
   - Note the autofilled slug
   - (Optional) Group name
   - (Optional) UI Settings:
     - Launch URL (`blank://blank` to hide)
     - `Open in new tab`
3. Click `Next` → Select `OAuth2/OIDC` → `Next`
4. Configure provider:
   - Client Type: `Confidential`
   - Note `ClientID` & `Client Secret`
   - (Optional) Redirect URIs/Origins
   - Select signing key (e.g., Cloudflare Cert)
5. Advanced Settings:
   - Scopes: Select `email`, `openid`, `profile`, `offline_access`
   - Subject Mode: `Based on User's Email`
6. Click `Next` to finish

## Section 3: Application Group Permissions

1. Navigate to `Applications > Applications`
2. Select desired application (click name)
3. Go to `Policy/Group/User Bindings` tab
4. Configure access:
   - Click `Bind Existing Policy`
     - Type: `Group`
     - Select `authentik Admins`
     - Order: `0`
     - Click `Create`
   - Repeat for additional groups:
     - Select group (e.g., "Plex Users")
     - Increment order (e.g., `10`)
     - Click `Create`

## Conclusion

This guide covers:
- Cloudflare certificate integration
- Application and provider setup
- Outpost configuration
- Group-based access control