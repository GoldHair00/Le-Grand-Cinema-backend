# Convention de nommage des branches

| Branche | Rôle | Exemple |
|---|---|---|
| main | Code stable, déployé en production | main |
| develop | Intégration des fonctionnalités | develop |
| feature/<nom> | Nouvelle user story | feature/login-user |
| fix/<nom> | Correction de bug | fix/double-booking |
| hotfix/<nom> | Correction urgente depuis main | hotfix/auth-token |
| docs/<nom> | Documentation | docs/swagger |

Règles : minuscules, mots séparés par des tirets, nom court et explicite.

Flux : feature/* → merge request vers develop → develop vers main à chaque livraison.

# Convention de commits

| Préfixe | Usage |
|---|---|
| feat: | nouvelle fonctionnalité |
| fix: | correction de bug |
| docs: | documentation |
| test: | tests |
| chore: | maintenance |