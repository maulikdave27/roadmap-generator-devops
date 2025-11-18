# AI Career Roadmap Generator

A Flask web app that generates personalized career learning roadmaps using Google's Gemini AI. Submit any career goal (like "Data Scientist" or "DevOps Engineer"), and get a structured, phase-by-phase learning plan tailored to help you reach that goal.

## What This Does

This project takes user input about their career goals and uses Google's Gemini API to create detailed learning roadmaps. The roadmaps are broken down into phases (beginner, intermediate, advanced) with actionable steps at each level.

The whole thing is built with DevOps in mind - there are multiple deployment options included, from simple Docker containers to full CI/CD pipelines with Jenkins, Kubernetes deployments, and Ansible automation.

## Tech Stack

**Backend:**
- Flask (Python web framework)
- Google Generative AI (Gemini API)
- Gunicorn (production server)
- Markdown (for formatting roadmap output)

**Frontend:**
- Plain HTML/CSS with Material Design 3 styling
- Inter font from Google Fonts
- Responsive design

**DevOps & Infrastructure:**
- Docker & Docker Compose
- Kubernetes (deployment manifests included)
- Jenkins (CI/CD pipeline)
- Ansible (automated deployment playbook)
- Terraform (AWS ECR setup)
- AWS ECR (container registry)

## Getting Started

### Prerequisites

You'll need:
- Python 3.11 or higher
- A Google Gemini API key (get one at [Google AI Studio](https://makersuite.google.com/app/apikey))
- Docker (optional, for containerized deployment)

### Local Development

1. Clone the repo:
```bash
git clone https://github.com/maulikdave27/roadmap-generator-devops.git
cd roadmap-generator-devops
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set your API key:
```bash
export GEMINI_API_KEY="your-api-key-here"
```

4. Run the app:
```bash
python app.py
```

5. Open your browser to `http://localhost:8080`

That's it! Type in a career goal and hit "Generate Roadmap" to see it in action.

### Using Docker

If you prefer Docker:

```bash
docker build -t roadmap-generator .
docker run -p 8080:8080 -e GEMINI_API_KEY="your-api-key" roadmap-generator
```

Or use docker-compose:

```bash
export GEMINI_API_KEY="your-api-key"
docker-compose up
```

## Project Structure

```
.
├── app.py                  # Main Flask application
├── index.html              # Frontend template
├── style.css               # Styling
├── requirements.txt        # Python dependencies
├── dockerfile              # Docker image definition
├── docker-compose.yml      # Docker Compose config
├── jenkinsfile             # Jenkins CI/CD pipeline
├── deployment.yml          # Kubernetes deployment manifest
├── deploy.yml              # Ansible playbook
├── hosts.ini               # Ansible inventory
└── main.tf                 # Terraform for AWS ECR
```

## How It Works

The app has two main routes:

1. **Web Interface** (`/`)
   - Shows a simple form where you enter your career goal
   - Displays the generated roadmap right on the page

2. **REST API** (`/api/roadmap`)
   - POST endpoint that accepts JSON: `{"goal": "your career goal"}`
   - Returns JSON with the generated roadmap

When you submit a goal, the app:
1. Takes your input and creates a prompt for Gemini
2. Sends the prompt to Google's Gemini 2.5 Flash model
3. Gets back a markdown-formatted roadmap
4. Converts the markdown to HTML
5. Displays it on the page (or returns it as JSON for the API)

## Deployment Options

### Option 1: Kubernetes

The `deployment.yml` file sets up:
- 2 replicas for high availability
- A LoadBalancer service exposing port 80
- API key stored in a Kubernetes secret

Create the secret first:
```bash
kubectl create secret generic gemini-secret --from-literal=api-key=YOUR_KEY
```

Then deploy:
```bash
kubectl apply -f deployment.yml
```

### Option 2: Jenkins CI/CD

The included `jenkinsfile` automates the entire deployment:
1. Checks out the code
2. Builds a Docker image
3. Pushes to AWS ECR
4. Deploys using Ansible

You'll need Jenkins configured with AWS credentials and access to your target server.

### Option 3: Ansible

The `deploy.yml` playbook handles:
- Installing Docker and dependencies on the target server
- Logging into AWS ECR
- Pulling the latest image
- Stopping any old containers
- Starting a new container with the app

Update `hosts.ini` with your server details, then run:
```bash
ansible-playbook -i hosts.ini deploy.yml
```

### Option 4: Infrastructure as Code

Use `main.tf` to create an ECR repository on AWS:
```bash
terraform init
terraform apply
```

This sets up image scanning and outputs the repository URL for your CI/CD pipeline.

## Configuration

The app reads configuration from environment variables:

- `GEMINI_API_KEY` (required) - Your Google Gemini API key
- `PORT` (optional) - Port to run on (default: 8080)
- `FLASK_ENV` (optional) - Set to "production" for production deployments

## API Usage Example

```bash
curl -X POST http://localhost:8080/api/roadmap \
  -H "Content-Type: application/json" \
  -d '{"goal": "Full Stack Developer"}'
```

Response:
```json
{
  "goal": "Full Stack Developer",
  "roadmap": "<html formatted roadmap content>"
}
```

## Security Notes

- Never commit API keys to the repository
- The `deploy.yml` file contains a hardcoded API key and AWS account ID - these should be moved to secrets management
- Image scanning is enabled in the ECR Terraform configuration
- Use environment variables or Kubernetes secrets for sensitive data in production

## Testing

The project includes pytest and bandit in requirements:

```bash
# Run tests (if any are added)
pytest

# Security scanning
bandit -r app.py
```

## Contributing

This is a learning project focused on DevOps practices. Feel free to fork it and experiment with:
- Adding more deployment options
- Improving the UI
- Adding caching for roadmap results
- Setting up monitoring and logging
- Implementing rate limiting

## License

This project is open source and available for educational purposes.

## Notes

The Jenkins pipeline assumes:
- An AWS ECR repository at the specified URL
- An EC2 instance configured in `hosts.ini`
- Jenkins has AWS CLI configured with proper credentials
- The target server has Docker installed

The roadmap generation uses Gemini 2.5 Flash with a prompt designed to give medium-length, phase-based responses. You can adjust the prompt in `app.py` if you want different output styles or lengths.
