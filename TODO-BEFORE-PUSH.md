# TODO Before Push

This file lists placeholders and actions to take before the repo is pushed public.

**Delete this file before the final commit.**

## Placeholders to swap

Find `REPO_PLACEHOLDER` and replace with the real repo URL:

- Use `git@github.com:Automattic/design-skills.git` for clone targets
- Use `https://github.com/Automattic/design-skills` for owner URLs and links

Files to update:

- [ ] `README.md` — install instructions
- [ ] `plugins/design/README.md` — install instructions
- [ ] `.claude-plugin/marketplace.json` — `owner.url`
- [ ] `plugins/design/skills/add-skill/SKILL.md` — clone target in Phase 2

Quick check: `grep -r REPO_PLACEHOLDER .`

## Steps after scaffolding

1. Create public repo via GitHub app: `github.com/Automattic/design-skills`
2. Swap all `REPO_PLACEHOLDER` references (above)
3. Delete this file
4. Stage and commit the placeholder swaps:
   ```
   git add -A
   git commit -m "chore: set repo URLs"
   ```
5. Add remote:
   ```
   git remote add origin git@github.com:Automattic/design-skills.git
   ```
6. Push:
   ```
   git push -u origin main
   ```
7. Tag:
   ```
   git tag design/v1.0.0
   git push --tags
   ```
8. Create release:
   ```
   gh release create design/v1.0.0 --title "design v1.0.0" --notes-file plugins/design/CHANGELOG.md
   ```
9. Reply in the `#design-meetup` Slack thread announcing the repo, ask David to contribute his 11 skills and Jill her Woo skills directly
10. Update the Field Guide page (`design-handbook/ai-design/claude-code-skills`) with the new install command
