# StuntShield - CICD

### Deploying model machine learning and APIs to Google Cloud Platform using Cloud Run.
Use Cloud Build to add trigger to GitHub repository then build a container image in Artifact Registry last deploying the container image to Cloud Run.

- Create service account for google cloud storage and cloud build set name and description then the other configuration:
  - For google cloud storage service account:
    - Grant this service account access to project (optional) (giving role):
      - Secret Manager Secret Accessor
      - Storage Admin
    - Grant users access to this service account (optional): Leave it default
  - For google cloud build service account:
    - Grant this service account access to project (optional) (giving role):
      - Artifact Registry Administrator
      - Cloud Build Service Account
      - Cloud Run Admin
      - Secret Manager Secret Accessor
      - Service Account User
      - Storage Object Admin
    - Grant users access to this service account (optional): Leave it default

- Create bucket in Cloud Bucket for storing output data prediction set name and region then the other configuration:
  - Set default class: Standard
  - Enforce public access prevention on this bucket: Uncheck
  - Access control: Fine-grained
  - Set other to default
- Create trigger in Cloud Build for connecting GitHub repository set name, region to us-central1 and description then the other configuration:
  - Event: Push to a branch
  - Source: 
    - Repository generation: 1st gen
    - Repository: GitHub repository name
    - Branch: GitHub branch name
    - Invert Regex: Uncheck
  - Configuration:
    - Type: Cloud Build configuration file (yaml or json)
    - Location: Repository
    - Cloud Build configuration file location: cloudbuild.yaml
  - Advanced:
    - Approval: Uncheck
    - Build logs: Uncheck
    - Service account: Service account for cloud build name

- Create repository in Artifact Registry set name then the other configuration:
  - Format: Docker
  - Mode: Standard
  - Location type: Region (it depends can also Multi-region)
  - Encryption: google-managed encryption key
  - Immutable image tags: Disable
  - Cleanup policies: dry run

- Storing all credential key to Secret Manager with configuration:
  - bucket-name: google storage bucket name
  - gcs-key: google cloud storage service account json key
  - openai-key: ChatGPT api key
  - searchengine-key: google search engine api key
