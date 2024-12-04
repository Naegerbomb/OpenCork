OpenCork is VERY MUCH a work in progress.  I'm beginning with standalone modules that can be run independently on data in batches for an MVP, then I'll work on making them more integrated and automated. 

# OpenCork

**OpenCork** is a set of open-source DtC-focused compliance tools designed for U.S.-based small wineries, crafted to simplify reporting and compliance processes while being free, accessible, and customizable. Built with Python, OpenCork focuses on providing essential compliance features without the complexity or cost of traditional compliance platforms meant for the wine industry.

---

## **Mission**

To empower wineries with an open-source solution that eliminates the high costs of compliance software, offers full control over data and processes, and encourages community-driven innovation.

---

## **Features**

1. **Tax Calculations**  
   - Automatically calculate state and regional taxes for shipments.  
   - Easily update tax rates via a simple configuration file.  

2. **Reporting**  
   - Generate customizable reports for tax filing and compliance tracking.  
   - Export reports in CSV or PDF formats.  
   - Provides a guided "walkthrough" for filing in each state, empowering you to "auto-file" on your own and save a ton of cash in just a few clicks.

3. **Age Verification**  
   - Securely process customer IDs for manual and/or automated age verification.
   - Access to a database of secure hashes representing verified customers.  Contribute to a community of DtC operators creating 100% free age verification.
   - Optional API integration for automated verification using paid 3rd party tools (e.g., IDology).  

4. **License Management**  
   - Track license details and renewal dates.  
   - Receive reminders for upcoming renewals.
   - Create draft emails for comliance partners like UPS and Fedex, so keep them informed about the latest changes to your wine shipping operation. 

5. **E-commerce Integration**  
   - Connect to platforms like Shopify or WooCommerce via CSV import/export and/or more automated methods.
   - Support customizable data mapping for seamless order compliance.  

6. **Real-Time Regulatory Updates**  
   - A community-driven wiki database of regulatory changes and fillable PDFs.  
   - Manual customization options for specific state requirements.  

7. **Manual Customization**  
   - Full control via a straightforward settings file (`config.json`).  
   - Customize workflows to suit your winery's unique needs.
   - Do compliance YOUR way, at YOUR speed, and at YOUR budget~!

---

## **Why OpenCork?**

- **Free and Open Source**: No subscriptions or hidden fees.  
- **Customizable**: Modify and adapt the software to fit your specific requirements.  
- **Accessible**: Designed with simplicity in mind, perfect for tech-savvy users or those looking for a powerful but free option. 
- **Community-Driven**: Collaborate, contribute, and innovate with other wineries.  

---

## **Getting Started**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/OpenCork.git
   cd OpenCork
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   python opencork.py
   ```

4. **Customize Settings**:  
   Edit the `config.json` file to configure tax rates, state rules, and other preferences.

---

## **Roadmap**

- Develop core compliance features (tax calculations, reporting, age verification).  
- Enhance ID verification with OCR and optional API support.  
- Build a simple CLI for seamless user interaction.  
- Add support for batch processing and e-commerce platform integration.  
- Expand documentation and tutorials for community contributions.  

---

## **Contributing**

We welcome contributions from developers, wineries, and compliance experts!  
- Submit bug reports or feature requests via GitHub Issues.  
- Fork the repository and create pull requests for enhancements.  

By contributing, you agree to release your work under the terms of the AGPL-3.0 license.

---

## **License**

This project is licensed under the [GNU Affero General Public License v3.0](LICENSE).  
You are free to use, modify, and distribute this software, but any modifications or network-distributed versions must also be released under the AGPL-3.0 license.

---

## **Contact**

Have questions or feedback? Reach out to the OpenCork team at [your-email@example.com].

Let’s make compliance easier—together!
