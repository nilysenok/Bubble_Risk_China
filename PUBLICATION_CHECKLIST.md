# GitHub Publication Checklist

Complete this checklist before publishing your replication package to GitHub.

## Pre-Publication Tasks

### 1. Update Placeholder Information

- [x] Replace `[Author Name]` with actual author name in:
  - [x] README.md → **S. M. Gavrikov and N. I. Lysenok**
  - [x] CITATION.cff → **S. M. Gavrikov and N. I. Lysenok**
  - [x] LICENSE → **S. M. Gavrikov and N. I. Lysenok**
  - [x] DATA_DICTIONARY.md → **S. M. Gavrikov and N. I. Lysenok**

- [x] Replace `[Author Institution]` with actual affiliation in:
  - [x] CITATION.cff → **HSE Moscow**

- [x] Replace `[your.email@institution.edu]` with actual email in:
  - [x] README.md → **nilysenok@hse.ru**
  - [x] DATA_DICTIONARY.md → **nilysenok@hse.ru**

- [x] Replace `YOUR-USERNAME` with actual GitHub username in:
  - [x] README.md → **nilysenok**
  - [x] CITATION.cff → **nilysenok**
  - [x] QUICKSTART.md → **nilysenok**

- [ ] Update DOI placeholder in:
  - [ ] README.md (line 161)
  - [ ] CITATION.cff (line 34)

- [ ] Update volume/issue/page numbers in:
  - [ ] README.md (lines 158-160)
  - [ ] CITATION.cff (lines 29-32)

- [ ] Update ORCID in CITATION.cff (lines 9, 24)

### 2. Verify Data Compliance

- [ ] Confirm all data sources allow public sharing
- [ ] Review Wind Financial Terminal terms of use
- [ ] Check Bloomberg data redistribution policy
- [ ] Verify compliance with Shanghai/Shenzhen Stock Exchange data policies
- [ ] Add any required data usage disclaimers

### 3. Code Review

- [ ] Test all scripts run successfully on clean install
- [ ] Verify output matches paper results (within tolerance)
- [ ] Check for hardcoded file paths (should use relative paths)
- [ ] Remove any sensitive information (API keys, credentials)
- [ ] Add comments to complex code sections
- [ ] Verify all imported libraries are in requirements.txt

### 4. Documentation Review

- [ ] Proofread README.md for typos
- [ ] Verify all file paths in documentation match actual structure
- [ ] Check that runtime estimates are accurate
- [ ] Ensure all figures/tables referenced exist
- [ ] Update "Last Updated" dates in all markdown files

### 5. Test Reproduction

- [ ] Clone package to fresh directory
- [ ] Install from requirements.txt in clean virtual environment
- [ ] Run all scripts in order
- [ ] Verify outputs match expected results
- [ ] Document any platform-specific issues
- [ ] Test on at least 2 different operating systems

## GitHub Setup

### 6. Create Repository

- [ ] Create new public repository: `DBN-FBD-China`
- [ ] Add description: "Replication package for 'Financial Bubble Detection in Chinese Stock Markets Using Dynamic Bayesian Networks' (CFRI 2025)"
- [ ] Add topics/tags: `finance`, `china`, `bubble-detection`, `bayesian-networks`, `machine-learning`, `replication-package`
- [ ] Initialize with README (or upload existing)

### 7. Repository Settings

- [ ] Enable Issues for user questions
- [ ] Add repository website (if paper has dedicated page)
- [ ] Configure branch protection (optional)
- [ ] Add collaborators (co-authors)

### 8. Upload Files

- [ ] Push all files from `GitHub_Replication_Package/`
- [ ] Verify .gitignore is working (no __pycache__, etc.)
- [ ] Check file sizes (GitHub has 100MB limit per file)
- [ ] Verify all folders and files appear correctly

### 9. Create Release

- [ ] Tag version as `v1.0.0`
- [ ] Write release notes summarizing package contents
- [ ] Attach ZIP archive of complete package
- [ ] Include DOI badge (after Zenodo archiving)

### 10. Add Badges to README

Update README.md header with badges:

```markdown
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
```

- [ ] Add Zenodo DOI badge
- [ ] Add license badge
- [ ] Add Python version badge

## Post-Publication

### 11. Archiving

- [ ] Archive repository on Zenodo for permanent DOI
- [ ] Update paper with GitHub URL
- [ ] Update paper with Zenodo DOI
- [ ] Submit data/code availability statement to journal

### 12. Promotion

- [ ] Tweet/share link to repository
- [ ] Add to Google Scholar profile
- [ ] List in CV/website
- [ ] Add to departmental resources
- [ ] Share with co-authors

### 13. Maintenance Plan

- [ ] Designate maintainer for issue responses
- [ ] Set up email notifications for GitHub issues
- [ ] Plan for periodic dependency updates
- [ ] Consider creating FAQ based on user questions

## Quality Checks

### 14. Final Verification

Run through this complete workflow on a fresh machine:

```bash
# Clone
git clone https://github.com/nilysenok/DBN-FBD-China.git
cd DBN-FBD-China

# Setup
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Run
cd code
python calculate_china_oct2025_real.py
python china_vs_usa_final_comparison.py
python generate_benchmark_comparison.py
python generate_robustness_checks.py
python generate_statistical_validation.py

# Verify outputs match paper
```

- [ ] Clone successful
- [ ] Installation successful (no errors)
- [ ] All scripts run without errors
- [ ] Outputs match paper results (within ±1%)
- [ ] Total runtime < 20 minutes

### 15. Accessibility

- [ ] README renders correctly on GitHub
- [ ] All images display properly
- [ ] Links work (no 404s)
- [ ] Code blocks have syntax highlighting
- [ ] Tables format correctly

### 16. Journal Requirements

- [ ] Check journal's data sharing policy
- [ ] Verify repository meets journal standards
- [ ] Include repository URL in manuscript
- [ ] Add data availability statement to paper
- [ ] Notify journal editor when package is live

## Common Issues to Check

- [ ] No absolute file paths (e.g., `/Users/yourname/...`)
- [ ] No hardcoded credentials or API keys
- [ ] All data files < 100MB (use Git LFS if larger)
- [ ] No proprietary/confidential data included
- [ ] Cross-platform compatibility (Windows paths, line endings)
- [ ] Python 2 vs 3 compatibility (use Python 3.8+)
- [ ] Consistent indentation (spaces vs tabs)
- [ ] UTF-8 encoding for all text files

## Optional Enhancements

Consider adding:

- [ ] Jupyter notebooks for interactive exploration
- [ ] Docker container for guaranteed reproducibility
- [ ] Continuous integration (GitHub Actions) to test on push
- [ ] Binder badge for browser-based execution
- [ ] Video tutorial walking through replication
- [ ] Slideshow presentation of results

## Contact Information for Help

If you encounter issues during publication:

- **GitHub Docs**: https://docs.github.com
- **Zenodo Help**: https://help.zenodo.org
- **Replication Package Best Practices**: https://social-science-data-editors.github.io/guidance/

---

## Final Sign-Off

Before going live, confirm:

- [ ] All placeholder text replaced
- [ ] All tests passing
- [ ] Co-authors reviewed and approved
- [ ] Journal notified (if required)
- [ ] Backup copy saved locally

**Publication Date**: _______________

**Published By**: S. M. Gavrikov and N. I. Lysenok

**Repository URL**: https://github.com/nilysenok/DBN-FBD-China

**Zenodo DOI**: _______________

---

**Congratulations on publishing your replication package!**

This transparent sharing of data and code significantly advances reproducible research in financial economics.
