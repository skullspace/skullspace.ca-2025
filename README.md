# SkullSpace Website and Blog

A Hugo-based static website and blog for [SkullSpace](https://skullspace.ca/), a hackerspace located in Winnipeg, Canada.

## About SkullSpace

SkullSpace is a hackerspace in Winnipeg, Manitoba, providing a collaborative environment for individuals interested in technology, art, and learning. Our community-driven space serves as a hub for innovation, creativity, and knowledge sharing.

## About This Project

This repository contains the source code for the SkullSpace website and blog, built with [Hugo](https://gohugo.io/), a fast and flexible static site generator written in Go.

## Prerequisites

Before you begin, ensure you have the following installed:

- [Hugo](https://gohugo.io/getting-started/installing/) (Extended version recommended)
- [Git](https://git-scm.com/)
- A text editor or IDE of your choice

## Getting Started

### Installation

1. **Clone the repository**:
   ```bash
   git clone git@github.com:skullspace/skullspace.ca-2025.git
   cd skullspace.ca-2025
   ```

2. **Install Hugo** (if not already installed):
   
   **macOS** (using Homebrew):
   ```bash
   brew install hugo
   ```
   
   **Linux**:
   ```bash
   sudo apt-get install hugo
   ```
   
   **Windows** (using Chocolatey):
   ```bash
   choco install hugo-extended
   ```
   
   For other installation methods, see the [Hugo installation guide](https://gohugo.io/getting-started/installing/).

### Development

1. **Start the development server**:
   ```bash
   hugo server
   ```
   
   Or with draft content and future posts:
   ```bash
   hugo server -D -F
   ```

2. **View the site**:
   Open your browser and navigate to `http://localhost:1313/`

3. **Stop the server**:
   Press `Ctrl+C` in the terminal

### Building for Production

To build the static site for production:

```bash
hugo
```

The generated site will be in the `public/` directory, ready to be deployed.

## Project Structure

```
.
├── archetypes/          # Content templates
├── content/             # Site content (pages, blog posts)
├── data/                # Data files (JSON, YAML, TOML)
├── layouts/             # HTML templates
├── static/              # Static assets (CSS, JS, images)
├── themes/              # Hugo themes
├── config.toml          # Site configuration
└── public/              # Generated static site (gitignored)
```

## Content Management

### Creating a New Blog Post

```bash
hugo new posts/my-new-post.md
```

### Creating a New Page

```bash
hugo new pages/my-new-page.md
```

## Contributing

We welcome contributions from the SkullSpace community! Here's how you can help:

1. **Fork the repository** on GitHub
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** and test them locally
4. **Commit your changes** with descriptive commit messages:
   ```bash
   git commit -m "Add: description of your changes"
   ```
5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Submit a pull request** on GitHub

Note that by contributing you agree to assign copyright to SkullSpace Winnipeg Inc. and abide the by [LICENSE](/LICENSE)

### Guidelines

- Follow existing code style and conventions
- Test your changes locally before submitting
- Write clear, descriptive commit messages
- Update documentation if needed
- Be respectful and constructive in discussions

## Deployment

The site is typically deployed automatically via CI/CD when changes are pushed to the main branch. For manual deployment:

1. Build the site: `hugo`
2. Deploy the contents of the `public/` directory to your hosting provider

Common hosting options:
- [GitHub Pages](https://pages.github.com/)
- [Cloudflare Pages](https://pages.cloudflare.com/)
- [Netlify](https://www.netlify.com/)
- [Vercel](https://vercel.com/)

## Resources

- [Hugo Documentation](https://gohugo.io/documentation/)
- [Hugo Themes](https://themes.gohugo.io/)
- [SkullSpace Website](https://skullspace.ca/)
- [SkullSpace Wiki](https://wiki.skullspace.ca/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions, suggestions, or support:

- **Email**: info@skullspace.ca
- **Website**: https://skullspace.ca/
- **Discord**: [Join our Discord server](https://discord.gg/nMwF43qrde)
- **Mailing List**: [Subscribe to our mailing list](https://skullspace.ca/mailing-list/)

## Acknowledgments

- Built with [Hugo](https://gohugo.io/)
- Maintained by the SkullSpace community
- Special thanks to all contributors and members
