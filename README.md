# 🏷️ Price Alerts

> **A powerful, intelligent price tracking system that monitors product prices across multiple e-commerce platforms with AI-powered scraping capabilities.**

[![Daily Scrape Job](https://github.com/D3N2-A/price-alerts/actions/workflows/scrape_job.yml/badge.svg)](https://github.com/D3N2-A/price-alerts/actions/workflows/scrape_job.yml)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-green.svg)](https://sqlalchemy.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue.svg)](https://postgresql.org)
[![AI-Powered](https://img.shields.io/badge/AI-Powered-orange.svg)](https://github.com/browser-use/browser-use)

## ✨ Features

### 🎯 **Smart Product Tracking**

- **Multi-Platform Support**: Native scrapers for Nike and Adidas
- **AI Fallback**: Intelligent AI-powered scraping for unsupported websites
- **Price History**: Complete historical price tracking with timestamps
- **Availability Monitoring**: Track product availability and stock status

### 🤖 **AI-Powered Intelligence**

- **Browser Automation**: Uses Google's Gemini 2.5 Flash for intelligent web scraping
- **Adaptive Scraping**: Automatically handles dynamic websites and anti-bot measures
- **Multi-Currency Support**: Supports INR, USD, EUR, GBP, JPY, KRW, and CNY

### 📊 **Data Management**

- **PostgreSQL Backend**: Robust database with proper relationships
- **Price History**: Track price changes over time
- **Product Metadata**: Store additional product information (offers, descriptions, etc.)
- **URL Validation**: Built-in URL validation and sanitization

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Main Script   │───▶│   Product URLs   │───▶│   Price DB      │
│   (main.py)     │    │   (Database)     │    │  (PostgreSQL)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       ▲
         ▼                       ▼                       │
┌─────────────────┐    ┌──────────────────┐              │
│   Scraper       │───▶│   Price History  │──────────────┘
│   (scrapper.py) │    │   (models.py)    │
└─────────────────┘    └──────────────────┘
         │
         ▼
┌─────────────────┐    ┌──────────────────┐
│  Nike/Adidas    │    │   AI Scraper     │
│   Scrapers      │    │  (Gemini 2.5)    │
└─────────────────┘    └──────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL database
- Google AI API key (for AI scraping)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/price-alerts.git
   cd price-alerts
   ```

2. **Install dependencies**

   ```bash
   pip install uv
   uv sync
   ```

3. **Environment Setup**
   Create a `.env` file in the project root:

   ```env
   POSTGRES_URL=postgresql://username:password@localhost:5432/price_alerts
   GOOGLE_API_KEY=your_google_ai_api_key_here
   ```

4. **Database Setup**
   The database tables will be automatically created on first run.

### Basic Usage

#### Adding Products to Track

```bash
python scripts/products.py
```

This interactive script allows you to add product URLs to your tracking list.

#### Running Price Scraping

```bash
python main.py
```

This will scrape all active products and update their price history.

## 🛠️ Advanced Usage

### Supported Platforms

#### Native Scrapers (Optimized)

- **Nike**: Direct DOM parsing with specific selectors
- **Adidas**: Custom scraper with availability detection

#### AI-Powered Universal Scraper

- **Any E-commerce Site**: Uses Google's Gemini 2.5 Flash model
- **Automatic Adaptation**: Handles dynamic content and anti-bot measures
- **Intelligent Parsing**: Extracts price, title, availability, and images

### Database Schema

```python
# Products Table
Product(
    url: str (primary_key),
    is_active: bool,
    is_deleted: bool
)

# Price History Table
PriceHistory(
    id: str (uuid),
    product_url: str (foreign_key),
    name: str,
    price: float,
    currency: str,
    main_image_url: str,
    availability: bool,
    timestamp: datetime,
    additional_data: dict
)
```

### Custom Scrapers

To add a new scraper for a specific website:

```python
class CustomScrapper(BaseScraper):
    def extract_title(self, soup: BeautifulSoup) -> str:
        # Implement title extraction
        pass

    def extract_price(self, soup: BeautifulSoup) -> float:
        # Implement price extraction
        pass

    def extract_availability(self, soup: BeautifulSoup) -> bool:
        # Implement availability check
        pass

    def extract_image_url(self, soup: BeautifulSoup) -> str:
        # Implement image URL extraction
        pass
```

## 📋 Configuration

### Currency Support

The system automatically detects and supports multiple currencies:

```python
currency_map = {
    "INR": ["₹", "INR"],
    "USD": ["$", "USD"],
    "EUR": ["€", "EUR"],
    "GBP": ["£", "GBP"],
    "JPY": ["¥", "JPY"],
    "KRW": ["₩", "KRW"],
    "CNY": ["¥", "CNY"],
}
```

### AI Scraper Configuration

The AI scraper can be customized by modifying the task prompt in `constants.py`:

```python
ai_scrapper_task = """
**AI Agent Task: Scrape the product information from the website**
# Customize this prompt for different scraping behaviors
"""
```

## 🔧 Development

### Project Structure

```
price-alerts/
├── main.py              # Main application entry point
├── scrapper.py          # Core scraping logic and scrapers
├── models.py            # SQLAlchemy models
├── db.py               # Database operations
├── constants.py        # Configuration and constants
├── scripts/
│   └── products.py     # Product management utilities
├── utils/
│   ├── url.py         # URL validation utilities
│   └── number.py      # Number parsing utilities
└── pyproject.toml     # Project dependencies
```

### Running Tests

```bash
# Add your test commands here
python -m pytest
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🤝 Use Cases

- **Personal Shopping**: Track favorite items for price drops
- **Inventory Management**: Monitor competitor pricing
- **Research**: Analyze pricing trends across platforms
- **Alerts**: Set up notifications for price changes (extend with notification system)

## 📊 Performance

- **Concurrent Scraping**: Uses ThreadPoolExecutor with 8 workers
- **Intelligent Fallbacks**: AI scraper for unsupported sites
- **Error Handling**: Robust error handling and logging
- **Database Optimization**: Efficient SQLAlchemy queries

## 🔮 Future Enhancements

- [ ] **Real-time Alerts**: Email/SMS notifications for price drops
- [ ] **Web Dashboard**: React/Vue.js frontend for data visualization
- [ ] **API Endpoints**: REST API for external integrations
- [ ] **Mobile App**: React Native mobile application
- [ ] **Machine Learning**: Price prediction algorithms
- [ ] **More Platforms**: Expand scraper support to Amazon, eBay, etc.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Browser Use](https://github.com/browser-use/browser-use) - AI-powered browser automation
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) - HTML parsing
- [SQLAlchemy](https://sqlalchemy.org/) - Database ORM
- [curl-cffi](https://github.com/yifeikong/curl_cffi) - HTTP client with browser impersonation

---

<div align="center">
  <strong>Built with ❤️ by developers, for smart shoppers</strong>
</div>
