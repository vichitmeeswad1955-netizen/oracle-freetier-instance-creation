name: OCI Free VM Grabber

on:
  workflow_dispatch:
  schedule:
    - cron: '0 */6 * * *'

jobs:
  grab-vm:
    runs-on: ubuntu-latest
    timeout-minutes: 350

    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Install dependencies
        run: pip install -r requirements.txt --quiet

      - name: Setup OCI Config
        run: |
          mkdir -p ~/.oci
          echo "${{ secrets.OCI_CONFIG }}" > ~/.oci/config
          echo "${{ secrets.OCI_KEY_FILE }}" > ~/.oci/oci_api_key.pem
          chmod 600 ~/.oci/config ~/.oci/oci_api_key.pem

      - name: Setup SSH Key
        run: |
          ssh-keygen -t rsa -b 2048 -f /home/runner/id_rsa -N ""
          chmod 644 /home/runner/id_rsa.pub

      - name: Run grabber
        run: python3 main.py
