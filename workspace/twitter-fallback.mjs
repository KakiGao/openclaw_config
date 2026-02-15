#!/usr/bin/env node
// twitter-fallback.mjs - 使用 Playwright 抓取 Twitter (无 Cookie 方案)

import { chromium } from 'playwright';

const SEARCH_TERMS = process.argv.slice(2) || ['AI Agents', 'AI tools'];

async function initBrowser() {
  const browser = await chromium.launch({
    headless: true,
    args: [
      '--disable-blink-features=AutomationControlled',
      '--no-sandbox',
      '--disable-dev-shm-usage',
      '--disable-gpu',
      '--disable-web-security',
      '--disable-features=IsolateOrigins,site-per-process'
    ]
  });

  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    viewport: { width: 1536, height: 800 },
    locale: 'en-US',
    timezoneId: 'America/New_York'
  });

  // 移除自动化特征
  await context.addInitScript(() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
    Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
    Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
    window.navigator.chrome = { runtime: {} };
  });

  return { browser, context };
}

async function searchWithRetry(page, query, maxRetries = 2) {
  const url = `https://twitter.com/search?q=${encodeURIComponent(query)}&src=typed_query&f=live`;
  
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      console.log(`   尝试 ${attempt}/${maxRetries}...`);
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
      await page.waitForTimeout(4000);
      
      // 滚动加载
      await page.evaluate(() => window.scrollTo(0, 300));
      await page.waitForTimeout(2000);
      
      // 检查是否被阻止
      const blocked = await page.$('text=rate limit') || await page.$('text=Too many requests');
      if (blocked) {
        console.log('   ⚠️ 被限流，等待后重试...');
        await page.waitForTimeout(5000);
        continue;
      }
      
      // 检查登录墙
      const loginWall = await page.$('input[name="text"]') || await page.$('[data-testid="LoginForm"]');
      if (loginWall) {
        console.log('   ⚠️ 登录墙 - 需要认证');
        return [];
      }
      
      // 查找推文 - 尝试多种选择器
      const selectors = [
        'article[data-testid="tweet"]',
        'div[data-testid="cellInnerDiv"]',
        'div[role="group"][aria-label]'
      ];
      
      for (const sel of selectors) {
        const tweets = await page.$$(sel);
        if (tweets.length > 0) {
          console.log(`   ✅ 找到 ${tweets.length} 条 (${sel})`);
          return tweets.slice(0, 5);
        }
      }
      
      console.log('   ⚠️ 未找到推文元素');
      return [];
      
    } catch (e) {
      console.log(`   ❌ 错误: ${e.message.slice(0, 50)}`);
      if (attempt < maxRetries) await page.waitForTimeout(3000);
    }
  }
  return [];
}

async function parseTweets(tweets) {
  const results = [];
  
  for (const tweet of tweets) {
    try {
      // 获取内容
      const contentEl = await tweet.$('[data-testid="tweetText"]') || 
                        await tweet.$('div[lang]') ||
                        await tweet.$('span');
      const content = contentEl ? await contentEl.textContent() : '';
      
      // 获取作者
      const authorEl = await tweet.$eval('a[href*="/"]', a => a.textContent).catch(() => '');
      const handle = authorEl.replace('@', '').trim();
      
      if (content && handle && content.length > 10) {
        results.push({
          handle,
          content: content.slice(0, 140) + (content.length > 140 ? '...' : '')
        });
      }
    } catch (e) {
      // 跳过解析失败的推文
    }
  }
  
  return results;
}

async function main() {
  console.log('🕵️ Twitter Fallback 模式 (无 Cookie)\n');
  
  let browser;
  try {
    const { browser: b } = await initBrowser();
    browser = b;
    const context = browser.contexts()[0];
    const page = await context.newPage();
    
    const allResults = {};
    
    for (const term of SEARCH_TERMS) {
      console.log(`\n📌 ${term}:`);
      const tweets = await searchWithRetry(page, term);
      const parsed = await parseTweets(tweets);
      allResults[term] = parsed;
      
      if (parsed.length === 0) {
        console.log('   (无结果)');
      } else {
        for (const t of parsed) {
          console.log(`   - **@${t.handle}**: ${t.content}`);
        }
      }
      
      // 避免请求过快
      await page.waitForTimeout(2000);
    }
    
    // 返回状态
    const hasResults = Object.values(allResults).some(arr => arr.length > 0);
    process.exit(hasResults ? 0 : 1);
    
  } catch (e) {
    console.error('❌ 严重错误:', e.message);
    process.exit(1);
  } finally {
    if (browser) await browser.close();
  }
}

main();
