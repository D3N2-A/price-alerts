session_headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Cache-Control": "max-age=0",
    "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"macOS"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "Connection": "keep-alive",
    "DNT": "1",
}

currency_map = {
    "INR": ["₹", "INR"],
    "USD": ["$", "USD"],
    "EUR": ["€", "EUR"],
    "GBP": ["£", "GBP"],
    "JPY": ["¥", "JPY"],
    "KRW": ["₩", "KRW"],
    "CNY": ["¥", "CNY"],
}


ai_scrapper_task = """
**AI Agent Task: Scrape the product information from the website**

**Objective:**  
Gather information on available product from the website: {url} and return information in structured format.  
[IMPORTANT] Follow the key requirements and output format.
---
**Instructions:**
1. Open the website {url} in the browser.
2. Check the product title and price with currency.
3. Check the product availability.
4. Check the product image url.
5. Check for additional information like offer, sold out text, etc.
6. Return the product information in structured format.

**Output Format:**
Return ONLY a valid JSON object with the following structure:
{{
    "title": "<Product Title>",
    "price": "<Product Price>",
    "currency": "<Product Currency>",
    "availability": "<Product Availability>",
    "image_url": "<Product Image URL>",
    "additional_data": {{
        "offer": "<Product Offer>",
        "sold_out_text": "<Product Sold Out Text>"
    }}
}}

**IMPORTANT KEY REQUIREMENTS:**
- Return ONLY the JSON object, no other text or formatting
- Ensure all values are strings except 'availability' which should be a boolean
- Do not include ```json or ``` markers in the response
- Make sure additional_data is dictionary, if not return empty dictionary
- Do not include any explanatory text or comments
"""
