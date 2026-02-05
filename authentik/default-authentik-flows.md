---
description: Default Authentik flows pulled directly from Authentik's Website.
---

# Default Authentik Flows

These flows are predefined flows pulled straight from the Authentik Website.

### Flows Enrollment - 2 Stage

<pre class="language-yaml" data-expandable="true"><code class="lang-yaml"><strong>## flows-enrollment-2-stage.yml
</strong><strong>version: 1
</strong>metadata:
  labels:
    blueprints.goauthentik.io/instantiate: "false"
  name: Example - Enrollment (2 Stage)
entries:
  - identifiers:
      slug: default-enrollment-flow
    model: authentik_flows.flow
    id: flow
    attrs:
      name: Default enrollment Flow
      title: Welcome to authentik!
      designation: enrollment
      authentication: require_unauthenticated
  - id: prompt-field-username
    model: authentik_stages_prompt.prompt
    identifiers:
      name: default-enrollment-field-username
    attrs:
      field_key: username
      label: Username
      type: username
      required: true
      placeholder: Username
      placeholder_expression: false
      order: 0
  - identifiers:
      name: default-enrollment-field-password
    id: prompt-field-password
    model: authentik_stages_prompt.prompt
    attrs:
      field_key: password
      label: Password
      type: password
      required: true
      placeholder: Password
      placeholder_expression: false
      order: 0
  - identifiers:
      name: default-enrollment-field-password-repeat
    id: prompt-field-password-repeat
    model: authentik_stages_prompt.prompt
    attrs:
      field_key: password_repeat
      label: Password (repeat)
      type: password
      required: true
      placeholder: Password (repeat)
      placeholder_expression: false
      order: 1
  - identifiers:
      name: default-enrollment-field-name
    id: prompt-field-name
    model: authentik_stages_prompt.prompt
    attrs:
      field_key: name
      label: Name
      type: text
      required: true
      placeholder: Name
      placeholder_expression: false
      order: 0
  - identifiers:
      name: default-enrollment-field-email
    id: prompt-field-email
    model: authentik_stages_prompt.prompt
    attrs:
      field_key: email
      label: Email
      type: email
      required: true
      placeholder: Email
      placeholder_expression: false
      order: 1
  - identifiers:
      name: default-enrollment-prompt-second
    id: default-enrollment-prompt-second
    model: authentik_stages_prompt.promptstage
    attrs:
      fields:
        - !KeyOf prompt-field-name
        - !KeyOf prompt-field-email
  - identifiers:
      name: default-enrollment-prompt-first
    id: default-enrollment-prompt-first
    model: authentik_stages_prompt.promptstage
    attrs:
      fields:
        - !KeyOf prompt-field-username
        - !KeyOf prompt-field-password
        - !KeyOf prompt-field-password-repeat
  - identifiers:
      name: default-enrollment-user-login
    id: default-enrollment-user-login
    model: authentik_stages_user_login.userloginstage
  - identifiers:
      name: default-enrollment-user-write
    id: default-enrollment-user-write
    model: authentik_stages_user_write.userwritestage
    attrs:
      user_creation_mode: always_create
  - identifiers:
      target: !KeyOf flow
      stage: !KeyOf default-enrollment-prompt-first
      order: 10
    model: authentik_flows.flowstagebinding
  - identifiers:
      target: !KeyOf flow
      stage: !KeyOf default-enrollment-prompt-second
      order: 11
    model: authentik_flows.flowstagebinding
  - identifiers:
      target: !KeyOf flow
      stage: !KeyOf default-enrollment-user-write
      order: 20
    model: authentik_flows.flowstagebinding
  - identifiers:
      target: !KeyOf flow
      stage: !KeyOf default-enrollment-user-login
      order: 100
    model: authentik_flows.flowstagebinding
</code></pre>

### Flows Enrollment Email Verification

{% code expandable="true" %}
```yaml
version: 1
metadata:
  labels:
    blueprints.goauthentik.io/instantiate: "false"
  name: Example - Enrollment with email verification
entries:
  - identifiers:
      slug: default-enrollment-flow
    id: flow
    model: authentik_flows.flow
    attrs:
      name: Default enrollment Flow
      title: Welcome to authentik!
      designation: enrollment
      authentication: require_unauthenticated
  - identifiers:
      name: default-enrollment-field-username
    id: prompt-field-username
    model: authentik_stages_prompt.prompt
    attrs:
      field_key: username
      label: Username
      type: username
      required: true
      placeholder: Username
      placeholder_expression: false
      order: 0
  - identifiers:
      name: default-enrollment-field-password
    id: prompt-field-password
    model: authentik_stages_prompt.prompt
    attrs:
      field_key: password
      label: Password
      type: password
      required: true
      placeholder: Password
      placeholder_expression: false
      order: 0
  - identifiers:
      name: default-enrollment-field-password-repeat
    id: prompt-field-password-repeat
    model: authentik_stages_prompt.prompt
    attrs:
      field_key: password_repeat
      label: Password (repeat)
      type: password
      required: true
      placeholder: Password (repeat)
      placeholder_expression: false
      order: 1
  - identifiers:
      name: default-enrollment-field-name
    id: prompt-field-name
    model: authentik_stages_prompt.prompt
    attrs:
      field_key: name
      label: Name
      type: text
      required: true
      placeholder: Name
      placeholder_expression: false
      order: 0
  - identifiers:
      name: default-enrollment-field-email
    id: prompt-field-email
    model: authentik_stages_prompt.prompt
    attrs:
      field_key: email
      label: Email
      type: email
      required: true
      placeholder: Email
      placeholder_expression: false
      order: 1
  - identifiers:
      name: default-enrollment-email-verification
    id: default-enrollment-email-verification
    model: authentik_stages_email.emailstage
    attrs:
      use_global_settings: true
      template: email/account_confirmation.html
      activate_user_on_success: true
  - identifiers:
      name: default-enrollment-prompt-second
    id: default-enrollment-prompt-second
    model: authentik_stages_prompt.promptstage
    attrs:
      fields:
        - !KeyOf prompt-field-name
        - !KeyOf prompt-field-email
  - identifiers:
      name: default-enrollment-prompt-first
    id: default-enrollment-prompt-first
    model: authentik_stages_prompt.promptstage
    attrs:
      fields:
        - !KeyOf prompt-field-username
        - !KeyOf prompt-field-password
        - !KeyOf prompt-field-password-repeat
  - identifiers:
      name: default-enrollment-user-login
    id: default-enrollment-user-login
    model: authentik_stages_user_login.userloginstage
  - identifiers:
      name: default-enrollment-user-write
    id: default-enrollment-user-write
    model: authentik_stages_user_write.userwritestage
    attrs:
      create_users_as_inactive: true
      user_creation_mode: always_create
  - identifiers:
      target: !KeyOf flow
      stage: !KeyOf default-enrollment-prompt-first
      order: 10
    model: authentik_flows.flowstagebinding
  - identifiers:
      target: !KeyOf flow
      stage: !KeyOf default-enrollment-prompt-second
      order: 11
    model: authentik_flows.flowstagebinding
  - identifiers:
      target: !KeyOf flow
      stage: !KeyOf default-enrollment-user-write
      order: 20
    model: authentik_flows.flowstagebinding
  - identifiers:
      target: !KeyOf flow
      stage: !KeyOf default-enrollment-email-verification
      order: 30
    model: authentik_flows.flowstagebinding
  - identifiers:
      target: !KeyOf flow
      stage: !KeyOf default-enrollment-user-login
      order: 100
    model: authentik_flows.flowstagebinding
```
{% endcode %}

### Flows Login - 2FA

{% code expandable="true" %}
```yml
version: 1
metadata:
  labels:
    blueprints.goauthentik.io/instantiate: "false"
  name: Example - Two-factor Login
entries:
  - identifiers:
      slug: default-authentication-flow
    model: authentik_flows.flow
    id: flow
    attrs:
      name: Default Authentication Flow
      title: Welcome to authentik!
      designation: authentication
      authentication: require_unauthenticated
  - identifiers:
      name: test-not-app-password
    id: test-not-app-password
    model: authentik_policies_expression.expressionpolicy
    attrs:
      expression: |
        return context.get("auth_method") != "app_password"
  - identifiers:
      name: default-authentication-login
    id: default-authentication-login
    model: authentik_stages_user_login.userloginstage
  - identifiers:
      name: default-authentication-identification
    id: default-authentication-identification
    model: authentik_stages_identification.identificationstage
    attrs:
      user_fields:
        - email
        - username
      template: stages/identification/login.html
  - identifiers:
      name: default-authentication-flow-mfa
    id: default-authentication-flow-mfa
    model: authentik_stages_authenticator_validate.authenticatorvalidatestage
  - identifiers:
      name: default-authentication-password
    id: default-authentication-password
    model: authentik_stages_password.passwordstage
    attrs:
      backends:
        - authentik.core.auth.InbuiltBackend
        - authentik.core.auth.TokenBackend
        - authentik.sources.ldap.auth.LDAPBackend
  - identifiers:
      target: !KeyOf flow
      stage: !KeyOf default-authentication-identification
      order: 10
    model: authentik_flows.flowstagebinding
  - identifiers:
      target: !KeyOf flow
      stage: !KeyOf default-authentication-password
      order: 20
    model: authentik_flows.flowstagebinding
  - identifiers:
      target: !KeyOf flow
      stage: !KeyOf default-authentication-flow-mfa
      order: 30
    model: authentik_flows.flowstagebinding
    id: flow-binding-mfa
    attrs:
      re_evaluate_policies: true
  - identifiers:
      target: !KeyOf flow
      stage: !KeyOf default-authentication-login
      order: 100
    model: authentik_flows.flowstagebinding
  - identifiers:
      policy: !KeyOf test-not-app-password
      target: !KeyOf flow-binding-mfa
      order: 0
    model: authentik_policies.policybinding
```
{% endcode %}

### Conditional Captcha

{% code expandable="true" %}
```yml
version: 1
metadata:
  labels:
    blueprints.goauthentik.io/instantiate: "false"
  name: Example - Login with conditional Captcha
entries:
  - identifiers:
      slug: default-authentication-flow
    id: flow
    model: authentik_flows.flow
    attrs:
      name: Default Authentication Flow
      title: Welcome to authentik!
      designation: authentication
      authentication: require_unauthenticated
  - identifiers:
      name: default-authentication-login
    id: default-authentication-login
    model: authentik_stages_user_login.userloginstage
  - identifiers:
      name: default-authentication-flow-captcha
    id: default-authentication-flow-captcha
    model: authentik_stages_captcha.captchastage
    attrs:
      public_key: 6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI
      private_key: 6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe
  - identifiers:
      name: default-authentication-identification
    id: default-authentication-identification
    model: authentik_stages_identification.identificationstage
    attrs:
      user_fields:
        - email
        - username
      template: stages/identification/login.html
  - identifiers:
      name: default-authentication-password
    id: default-authentication-password
    model: authentik_stages_password.passwordstage
    attrs:
      backends:
        - authentik.core.auth.InbuiltBackend
        - authentik.core.auth.TokenBackend
        - authentik.sources.ldap.auth.LDAPBackend
  - identifiers:
      target: !KeyOf flow
      stage: !KeyOf default-authentication-identification
      order: 10
    model: authentik_flows.flowstagebinding
  - identifiers:
      target: !KeyOf flow
      stage: !KeyOf default-authentication-password
      order: 20
    model: authentik_flows.flowstagebinding
  - identifiers:
      target: !KeyOf flow
      stage: !KeyOf default-authentication-flow-captcha
      order: 30
    id: flow-binding-captcha
    model: authentik_flows.flowstagebinding
    attrs:
      evaluate_on_plan: false
      re_evaluate_policies: true
  - identifiers:
      target: !KeyOf flow
      stage: !KeyOf default-authentication-login
      order: 100
    model: authentik_flows.flowstagebinding
  - identifiers:
      name: default-authentication-flow-conditional-captcha
    id: default-authentication-flow-conditional-captcha
    model: authentik_policies_reputation.reputationpolicy
    attrs:
      check_ip: true
      check_username: true
      threshold: -5
  - identifiers:
      policy: !KeyOf default-authentication-flow-conditional-captcha
      target: !KeyOf flow-binding-captcha
      order: 0
    model: authentik_policies.policybinding
```
{% endcode %}

### Flows Recovery Email Verification

{% code expandable="true" %}
```yml
version: 1
metadata:
  labels:
    blueprints.goauthentik.io/instantiate: "false"
  name: Example - Recovery with email verification
entries:
  - identifiers:
      slug: default-recovery-flow
    id: flow
    model: authentik_flows.flow
    attrs:
      name: Default recovery flow
      title: Reset your password
      designation: recovery
      authentication: require_unauthenticated
  - identifiers:
      name: default-recovery-field-password
    id: prompt-field-password
    model: authentik_stages_prompt.prompt
    attrs:
      field_key: password
      label: Password
      type: password
      required: true
      placeholder: Password
      order: 0
      placeholder_expression: false
  - identifiers:
      name: default-recovery-field-password-repeat
    id: prompt-field-password-repeat
    model: authentik_stages_prompt.prompt
    attrs:
      field_key: password_repeat
      label: Password (repeat)
      type: password
      required: true
      placeholder: Password (repeat)
      order: 1
      placeholder_expression: false
  - identifiers:
      name: default-recovery-skip-if-restored
    id: default-recovery-skip-if-restored
    model: authentik_policies_expression.expressionpolicy
    attrs:
      expression: |
        return bool(request.context.get('is_restored', True))
  - identifiers:
      name: default-recovery-email
    id: default-recovery-email
    model: authentik_stages_email.emailstage
    attrs:
      use_global_settings: true
      host: localhost
      port: 25
      username: ""
      use_tls: false
      use_ssl: false
      timeout: 10
      from_address: system@authentik.local
      token_expiry: 30
      subject: authentik
      template: email/password_reset.html
      activate_user_on_success: true
  - identifiers:
      name: default-recovery-user-write
    id: default-recovery-user-write
    model: authentik_stages_user_write.userwritestage
    attrs:
      user_creation_mode: never_create
  - identifiers:
      name: default-recovery-identification
    id: default-recovery-identification
    model: authentik_stages_identification.identificationstage
    attrs:
      user_fields:
        - email
        - username
  - identifiers:
      name: default-recovery-user-login
    id: default-recovery-user-login
    model: authentik_stages_user_login.userloginstage
  - identifiers:
      name: Change your password
    id: stages-prompt-password
    model: authentik_stages_prompt.promptstage
    attrs:
      fields:
        - !KeyOf prompt-field-password
        - !KeyOf prompt-field-password-repeat
      validation_policies: []
  - identifiers:
      target: !KeyOf flow
      stage: !KeyOf default-recovery-identification
      order: 10
    model: authentik_flows.flowstagebinding
    id: flow-binding-identification
    attrs:
      evaluate_on_plan: true
      re_evaluate_policies: true
      policy_engine_mode: any
      invalid_response_action: retry
  - identifiers:
      target: !KeyOf flow
      stage: !KeyOf default-recovery-email
      order: 20
    model: authentik_flows.flowstagebinding
    id: flow-binding-email
    attrs:
      evaluate_on_plan: true
      re_evaluate_policies: true
      policy_engine_mode: any
      invalid_response_action: retry
  - identifiers:
      pk: 1219d06e-2c06-4c5b-a162-78e3959c6cf0
      target: !KeyOf flow
      stage: !KeyOf stages-prompt-password
      order: 30
    model: authentik_flows.flowstagebinding
    attrs:
      evaluate_on_plan: true
      re_evaluate_policies: false
      policy_engine_mode: any
      invalid_response_action: retry
  - identifiers:
      target: !KeyOf flow
      stage: !KeyOf default-recovery-user-write
      order: 40
    model: authentik_flows.flowstagebinding
    attrs:
      evaluate_on_plan: true
      re_evaluate_policies: false
      policy_engine_mode: any
      invalid_response_action: retry
  - identifiers:
      target: !KeyOf flow
      stage: !KeyOf default-recovery-user-login
      order: 100
    model: authentik_flows.flowstagebinding
    attrs:
      evaluate_on_plan: true
      re_evaluate_policies: false
      policy_engine_mode: any
      invalid_response_action: retry
  - identifiers:
      policy: !KeyOf default-recovery-skip-if-restored
      target: !KeyOf flow-binding-identification
      order: 0
    model: authentik_policies.policybinding
    attrs:
      negate: false
      enabled: true
      timeout: 30
  - identifiers:
      policy: !KeyOf default-recovery-skip-if-restored
      target: !KeyOf flow-binding-email
      order: 0
    state: absent
    model: authentik_policies.policybinding
    attrs:
      negate: false
      enabled: true
      timeout: 30
```
{% endcode %}

### Flows Un-Enrollment

{% code expandable="true" %}
```yml
version: 1
metadata:
  labels:
    blueprints.goauthentik.io/instantiate: "false"
  name: Example - User deletion
entries:
  - identifiers:
      slug: default-unenrollment-flow
    model: authentik_flows.flow
    id: flow
    attrs:
      name: Default unenrollment flow
      title: Delete your account
      designation: unenrollment
      authentication: require_authenticated
  - identifiers:
      name: default-unenrollment-user-delete
    id: default-unenrollment-user-delete
    model: authentik_stages_user_delete.userdeletestage
    attrs: {}
  - identifiers:
      target: !KeyOf flow
      stage: !KeyOf default-unenrollment-user-delete
      order: 10
    model: authentik_flows.flowstagebinding
```
{% endcode %}
