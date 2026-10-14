/**
 * StockMind AI — Interactive Frontend Application Logic
 * Integrates Conversational Assistant, Plotly Financial Charts, Dashboard Cards,
 * Web Speech API (Voice Input & Text-to-Speech), and Real-time Market Polling.
 */

// Application State
const state = {
    activeSymbol: "TCS.NS",
    activeTimeframe: "1y",
    isRecording: false,
    selectedFile: null,
    speechRecognition: null,
    currentSpeechUtterance: null,
    chartInstances: {},
    companies: [],
    categories: {},
    activeModalCategory: "all",
    selectedAutocompleteIndex: -1,
    currentChatId: Date.now().toString()
};

// DOM Elements
const welcomeScreen = document.getElementById("welcome-screen");
const messageList = document.getElementById("message-list");
const chatForm = document.getElementById("chat-form");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const voiceBtn = document.getElementById("voice-btn");
const attachBtn = document.getElementById("attach-btn");
const fileInput = document.getElementById("file-input");
const attachmentPreview = document.getElementById("attachment-preview");
const attachmentName = document.getElementById("attachment-name");
const removeAttachmentBtn = document.getElementById("remove-attachment-btn");
const headerTickerStrip = document.getElementById("header-ticker-strip");
const marketOverviewBtn = document.getElementById("market-overview-btn");
const newChatBtn = document.getElementById("new-chat-btn");
const navHomeBtn = document.getElementById("nav-home-btn");
const companiesModalBtn = document.getElementById("companies-modal-btn");
const browseCompaniesBtn = document.getElementById("browse-companies-btn");
const companiesModal = document.getElementById("companies-modal");
const closeCompaniesModalBtn = document.getElementById("close-companies-modal-btn");
const companyModalSearchInput = document.getElementById("company-modal-search-input");
const modalCategoryTabs = document.getElementById("modal-category-tabs");
const companiesGridContainer = document.getElementById("companies-grid-container");
const chatboxAutocomplete = document.getElementById("chatbox-autocomplete");
const welcomeCategoriesBar = document.getElementById("welcome-categories-bar");
const welcomeChipsContainer = document.getElementById("welcome-chips-container");
const libraryBtn = document.getElementById("library-btn");
const libraryModal = document.getElementById("library-modal");
const libraryCloseBtn = document.getElementById("library-close-btn");
const libraryClearAllBtn = document.getElementById("library-clear-all-btn");
const librarySearchInput = document.getElementById("library-search-input");
const libraryListContainer = document.getElementById("library-list-container");

// Initialization
document.addEventListener("DOMContentLoaded", () => {
    initVoiceRecognition();
    fetchMarketTickerStrip();
    fetchCompaniesCatalog();
    setupEventHandlers();
    setupAutocompleteHandlers();
    setupCompaniesModalHandlers();
    setupWelcomeCategoryFilter();
    setupLibraryHandlers();
    updateLibraryBadge();
});

// Setup Event Handlers
function setupEventHandlers() {
    // Form submission
    chatForm.addEventListener("submit", (e) => {
        e.preventDefault();
        submitUserQuery();
    });

    // Enter key to send (Shift+Enter for newline)
    userInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            submitUserQuery();
        }
    });

    // Suggestion chips
    document.querySelectorAll(".chip").forEach(chip => {
        chip.addEventListener("click", () => {
            const query = chip.getAttribute("data-query");
            userInput.value = query;
            submitUserQuery();
        });
    });

    // Market Overview button
    marketOverviewBtn.addEventListener("click", () => {
        userInput.value = "How is the stock market today?";
        submitUserQuery();
    });

    // New Chat button & Home Logo
    const resetChat = () => {
        stopSpeaking();
        messageList.innerHTML = "";
        welcomeScreen.style.display = "flex";
        userInput.value = "";
        clearAttachment();
        state.activeSymbol = "TCS.NS";
        state.activeTimeframe = "1y";
        state.currentChatId = Date.now().toString();
    };
    newChatBtn.addEventListener("click", resetChat);
    navHomeBtn.addEventListener("click", resetChat);

    // File Attachment handlers
    attachBtn.addEventListener("click", () => fileInput.click());
    fileInput.addEventListener("change", (e) => {
        if (e.target.files && e.target.files[0]) {
            state.selectedFile = e.target.files[0];
            attachmentName.textContent = state.selectedFile.name;
            attachmentPreview.style.display = "flex";
        }
    });
    removeAttachmentBtn.addEventListener("click", clearAttachment);

    // Voice button handler
    voiceBtn.addEventListener("click", toggleVoiceRecognition);

    // Close Modal Button
    const closeModalBtn = document.getElementById("close-modal-btn");
    const chartModal = document.getElementById("chart-modal");
    if (closeModalBtn) {
        closeModalBtn.addEventListener("click", () => {
            chartModal.style.display = "none";
        });
    }
}

function clearAttachment() {
    state.selectedFile = null;
    fileInput.value = "";
    attachmentPreview.style.display = "none";
    attachmentName.textContent = "";
}

// Fetch and Render Global Market Ticker Strip
async function fetchMarketTickerStrip() {
    try {
        const res = await fetch("/api/market-overview");
        if (!res.ok) return;
        const data = await res.json();
        
        headerTickerStrip.innerHTML = "";
        if (data.indices && data.indices.length > 0) {
            data.indices.forEach(idx => {
                const item = document.createElement("div");
                item.className = "ticker-item";
                const isUp = idx.change >= 0;
                item.innerHTML = `
                    <span class="sym">${idx.name}</span>
                    <span class="val">${idx.currency_symbol}${idx.current_price.toLocaleString()}</span>
                    <span class="chg ${isUp ? 'up' : 'down'}">${idx.change_formatted}</span>
                `;
                item.addEventListener("click", () => {
                    userInput.value = `Analyze ${idx.name}`;
                    submitUserQuery();
                });
                headerTickerStrip.appendChild(item);
            });
        }
    } catch (err) {
        console.error("Failed to load market ticker strip:", err);
    }
}

// Web Speech API: Voice-to-Text
function initVoiceRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
        state.speechRecognition = new SpeechRecognition();
        state.speechRecognition.continuous = false;
        state.speechRecognition.interimResults = false;
        state.speechRecognition.lang = "en-IN"; // English/Indian locale

        state.speechRecognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            userInput.value = transcript;
            state.isRecording = false;
            voiceBtn.classList.remove("listening");
            submitUserQuery();
        };

        state.speechRecognition.onerror = (e) => {
            console.warn("Speech recognition error:", e);
            state.isRecording = false;
            voiceBtn.classList.remove("listening");
        };

        state.speechRecognition.onend = () => {
            state.isRecording = false;
            voiceBtn.classList.remove("listening");
        };
    } else {
        voiceBtn.style.opacity = "0.4";
        voiceBtn.title = "Voice recognition not supported in this browser";
    }
}

function toggleVoiceRecognition() {
    if (!state.speechRecognition) return;
    if (state.isRecording) {
        state.speechRecognition.stop();
        state.isRecording = false;
        voiceBtn.classList.remove("listening");
    } else {
        try {
            state.speechRecognition.start();
            state.isRecording = true;
            voiceBtn.classList.add("listening");
        } catch (err) {
            console.error("Speech start error:", err);
        }
    }
}

// Text-to-Speech: Read Aloud with Stop Button Support
function speakText(text, listenBtn, stopBtn) {
    if (!("speechSynthesis" in window)) return;
    window.speechSynthesis.cancel();
    resetAllAudioButtons();

    // Clean markdown symbols for natural speech
    const cleanSpeech = text
        .replace(/[*_#`~|]/g, " ")
        .replace(/\n+/g, ". ")
        .substring(0, 500); // Read first 500 characters of summary

    const utterance = new SpeechSynthesisUtterance(cleanSpeech);
    utterance.rate = 1.0;
    utterance.pitch = 1.0;

    if (listenBtn && stopBtn) {
        listenBtn.style.display = "none";
        stopBtn.style.display = "inline-flex";
    }

    const reset = () => {
        if (listenBtn && stopBtn) {
            listenBtn.style.display = "inline-flex";
            stopBtn.style.display = "none";
        }
    };

    utterance.onend = reset;
    utterance.onerror = reset;
    window.speechSynthesis.speak(utterance);
}

function stopSpeaking() {
    if ("speechSynthesis" in window) {
        window.speechSynthesis.cancel();
    }
    resetAllAudioButtons();
}

function resetAllAudioButtons() {
    document.querySelectorAll(".audio-listen-btn").forEach(b => b.style.display = "inline-flex");
    document.querySelectorAll(".audio-stop-btn").forEach(b => b.style.display = "none");
}

// Submit User Query
async function submitUserQuery() {
    const query = userInput.value.trim();
    if (!query && !state.selectedFile) return;

    // Hide welcome screen
    welcomeScreen.style.display = "none";

    // Append user message
    const displayQuery = query || (state.selectedFile ? `[Attached file: ${state.selectedFile.name}]` : "");
    appendUserMessage(displayQuery);

    // Reset input
    userInput.value = "";
    const attachedFile = state.selectedFile;
    clearAttachment();

    // Show loading assistant placeholder
    const loadingId = "loading-" + Date.now();
    appendLoadingMessage(loadingId);

    try {
        const payload = {
            query: displayQuery,
            active_symbol: state.activeSymbol,
            timeframe: state.activeTimeframe
        };

        const res = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (!res.ok) {
            const errData = await res.json().catch(() => ({}));
            throw new Error(errData.detail || "Error connecting to StockMind AI.");
        }

        const data = await res.json();
        removeLoadingMessage(loadingId);
        renderAssistantResponse(data);
        saveToLibrary(displayQuery, data);

    } catch (err) {
        removeLoadingMessage(loadingId);
        appendErrorMessage(err.message || "Failed to process query. Please try again.");
    }
}

// Append User Message to UI
function appendUserMessage(text) {
    const row = document.createElement("div");
    row.className = "message-wrapper user-message-row";
    row.innerHTML = `<div class="user-bubble">${escapeHtml(text)}</div>`;
    messageList.appendChild(row);
    scrollToBottom();
}

// Append Loading Skeleton
function appendLoadingMessage(id) {
    const row = document.createElement("div");
    row.className = "message-wrapper assistant-message-row";
    row.id = id;
    row.innerHTML = `
        <div class="assistant-avatar"><img src="/static/logo.png" alt="StockMind AI" class="avatar-logo-img"></div>
        <div class="assistant-content" style="padding: 18px 22px; border-left: 3px solid var(--purple-400);">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div class="loading-dots"><span></span><span></span><span></span></div>
                <span style="color: var(--text-muted); font-size: 13.5px; font-weight: 500;">StockMind AI is analyzing indicators &amp; predictions…</span>
            </div>
        </div>
    `;
    messageList.appendChild(row);
    scrollToBottom();
}

function removeLoadingMessage(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

function appendErrorMessage(errorMsg) {
    const row = document.createElement("div");
    row.className = "message-wrapper assistant-message-row";
    row.innerHTML = `
        <div class="assistant-avatar" style="background: var(--accent-red);">!</div>
        <div class="assistant-content" style="border-left: 4px solid var(--accent-red);">
            <div style="color: var(--accent-red); font-weight: 600; font-size: 14.5px;">Market Data Notice</div>
            <p style="font-size: 14px; color: var(--text-secondary); margin-top: 4px;">${escapeHtml(errorMsg)}</p>
        </div>
    `;
    messageList.appendChild(row);
    scrollToBottom();
}

// Render Assistant Response: WORDING FIRST -> NEXT PRICE -> NEXT GRAPH
function renderAssistantResponse(data) {
    const { text_response, stock_analysis, comparison, market_overview, intent, language } = data;

    if (stock_analysis && stock_analysis.quote) {
        state.activeSymbol = stock_analysis.quote.symbol;
    }

    const row = document.createElement("div");
    row.className = "message-wrapper assistant-message-row";

    const contentDiv = document.createElement("div");
    contentDiv.className = "assistant-content";

    // 1. Meta Bar (Live status & Read Aloud)
    const metaBar = document.createElement("div");
    metaBar.className = "assistant-meta-bar";
    
    let statusText = "Market Analysis";
    let statusClass = "green";
    if (stock_analysis && stock_analysis.quote) {
        statusText = `${stock_analysis.quote.symbol} • ${stock_analysis.quote.market_status_detail}`;
        statusClass = stock_analysis.quote.is_market_open ? "green" : "amber";
    }

    metaBar.innerHTML = `
        <div class="meta-status-pill">
            <span class="status-dot ${statusClass}"></span>
            <span>${escapeHtml(statusText)}</span>
        </div>
        <div class="audio-controls-group">
            <button type="button" class="audio-read-btn audio-listen-btn" title="Listen to response">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/></svg>
                <span>Listen</span>
            </button>
            <button type="button" class="audio-read-btn audio-stop-btn" style="display: none;" title="Stop reading aloud">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><rect x="5" y="5" width="14" height="14" rx="2"/></svg>
                <span>Stop</span>
            </button>
        </div>
    `;

    const listenBtn = metaBar.querySelector(".audio-listen-btn");
    const stopBtn = metaBar.querySelector(".audio-stop-btn");

    listenBtn.addEventListener("click", () => {
        speakText(text_response, listenBtn, stopBtn);
    });
    stopBtn.addEventListener("click", () => {
        stopSpeaking();
    });
    contentDiv.appendChild(metaBar);

    // =========================================================================
    // 2. [WORDING FIRST] AI Narrative, Technical Breakdown & Educational Verdict
    // =========================================================================
    const wordingSection = document.createElement("div");
    wordingSection.className = "response-section wording-section";
    wordingSection.innerHTML = `
        <div class="response-section-header">
            <span class="section-label">📝 Quantitative Analysis &amp; Insights</span>
        </div>
        <div class="markdown-body">
            ${marked.parse(text_response)}
        </div>
    `;
    contentDiv.appendChild(wordingSection);

    // =========================================================================
    // 3. [NEXT PRICE] Key Valuation & Financial Metrics Dashboard Grid
    // =========================================================================
    if (stock_analysis && stock_analysis.dashboard_cards && stock_analysis.dashboard_cards.length > 0) {
        const priceSection = document.createElement("div");
        priceSection.className = "response-section price-section";
        priceSection.innerHTML = `
            <div class="response-section-header">
                <span class="section-label">💰 Key Price &amp; Financial Metrics</span>
            </div>
        `;

        const grid = document.createElement("div");
        grid.className = "dashboard-grid";
        stock_analysis.dashboard_cards.forEach(c => {
            const cardEl = document.createElement("div");
            cardEl.className = "metric-card";
            cardEl.innerHTML = `
                <div class="card-header-row">
                    <span class="card-title">${escapeHtml(c.title)}</span>
                    <span class="card-badge">${escapeHtml(c.badge)}</span>
                </div>
                <div class="card-value ${c.tone}">${escapeHtml(c.value)}</div>
                <div class="card-subtext">${escapeHtml(c.subtext)}</div>
            `;
            grid.appendChild(cardEl);
        });
        priceSection.appendChild(grid);
        contentDiv.appendChild(priceSection);
    }

    // =========================================================================
    // 4. [NEXT GRAPH] Interactive Plotly Candlestick & Prediction Forecast Chart
    // =========================================================================
    if (stock_analysis && stock_analysis.chart_payload) {
        const chartId = "chart-" + Date.now();
        const chartSection = document.createElement("div");
        chartSection.className = "response-section chart-section";
        chartSection.innerHTML = `
            <div class="response-section-header">
                <span class="section-label">📈 Interactive Technical &amp; Forecast Chart</span>
            </div>
            <div class="embedded-chart-section">
                <div class="chart-header-bar">
                    <div class="chart-title-tag">
                        <span>${escapeHtml(stock_analysis.quote.name)}</span>
                        <span class="chart-pill">${escapeHtml(stock_analysis.quote.symbol)}</span>
                    </div>
                    <div class="timeframe-group" id="tf-group-${chartId}">
                        <button class="tf-btn" data-tf="1d">1D</button>
                        <button class="tf-btn" data-tf="5d">5D</button>
                        <button class="tf-btn" data-tf="1mo">1M</button>
                        <button class="tf-btn" data-tf="3mo">3M</button>
                        <button class="tf-btn" data-tf="6mo">6M</button>
                        <button class="tf-btn active" data-tf="1y">1Y</button>
                        <button class="tf-btn" data-tf="5y">5Y</button>
                    </div>
                </div>
                <div id="${chartId}" class="plotly-chart-box"></div>
            </div>
        `;
        contentDiv.appendChild(chartSection);

        // Render Plotly Chart after adding to DOM
        setTimeout(() => {
            renderPlotlyChart(chartId, stock_analysis.chart_payload, stock_analysis.quote);
            setupChartTimeframeButtons(chartId, stock_analysis.quote.symbol);
        }, 50);
    }

    // =========================================================================
    // 5. [NEXT COMPARISON GRAPH] If Stock Comparison Query
    // =========================================================================
    if (comparison && comparison.chart_data) {
        const compChartId = "comp-chart-" + Date.now();
        const compSection = document.createElement("div");
        compSection.className = "response-section chart-section";
        compSection.innerHTML = `
            <div class="response-section-header">
                <span class="section-label">🔄 Relative Performance (Base 100)</span>
            </div>
            <div class="embedded-chart-section">
                <div class="chart-header-bar">
                    <div class="chart-title-tag">
                        <span>Comparative Return Trajectory</span>
                        <span class="chart-pill">${comparison.stock_a.symbol} vs ${comparison.stock_b.symbol}</span>
                    </div>
                </div>
                <div id="${compChartId}" class="plotly-chart-box" style="min-height: 320px;"></div>
            </div>
        `;
        contentDiv.appendChild(compSection);

        setTimeout(() => {
            renderComparisonPlotlyChart(compChartId, comparison);
        }, 50);
    }

    // =========================================================================
    // 6. Interactive Quick Follow-up Action Chips
    // =========================================================================
    if (stock_analysis && stock_analysis.quote) {
        const sym = stock_analysis.quote.symbol;
        const name = stock_analysis.quote.name;
        const followup = document.createElement("div");
        followup.className = "followup-actions-strip";
        followup.innerHTML = `
            <span class="followup-label">Quick Actions:</span>
            <button type="button" class="action-chip" data-query="Explain ${name} in detail.">📊 Deep Technicals</button>
            <button type="button" class="action-chip" data-query="Why did ${name} move recently?">❓ Why did it move?</button>
            <button type="button" class="action-chip" data-query="What is the 5-day prediction for ${name}?">🔮 5-Day Target</button>
            <button type="button" class="action-chip" data-query="Compare ${name} and Infosys.">🔄 Compare with Peer</button>
        `;
        followup.querySelectorAll(".action-chip").forEach(btn => {
            btn.addEventListener("click", () => {
                userInput.value = btn.getAttribute("data-query");
                submitUserQuery();
            });
        });
        contentDiv.appendChild(followup);
    }

    row.innerHTML = `<div class="assistant-avatar"><img src="/static/logo.png" alt="StockMind AI" class="avatar-logo-img"></div>`;
    row.appendChild(contentDiv);
    messageList.appendChild(row);

    // Keep view at start of assistant response so output doesn't scroll all the way down
    row.scrollIntoView({ behavior: "smooth", block: "start" });
}

// Render Plotly Financial Candlestick & Forecast Chart
function renderPlotlyChart(elementId, payload, quote) {
    const el = document.getElementById(elementId);
    if (!el || !window.Plotly) return;

    const dates = payload.dates;
    const ohlc = payload.ohlc;
    const overlays = payload.overlays;
    const forecast = payload.forecast;

    const traces = [];

    // 1. Candlestick Trace
    traces.push({
        x: dates,
        open: ohlc.open,
        high: ohlc.high,
        low: ohlc.low,
        close: ohlc.close,
        type: 'candlestick',
        name: quote.symbol,
        increasing: { line: { color: '#10B981', width: 1.2 }, fillcolor: '#10B981' },
        decreasing: { line: { color: '#EF4444', width: 1.2 }, fillcolor: '#EF4444' },
        yaxis: 'y'
    });

    // 2. SMA 20
    if (overlays.sma_20 && overlays.sma_20.length > 0) {
        traces.push({
            x: dates,
            y: overlays.sma_20,
            type: 'scatter',
            mode: 'lines',
            name: 'SMA 20',
            line: { color: '#3B82F6', width: 1.5 },
            yaxis: 'y'
        });
    }

    // 3. SMA 50
    if (overlays.sma_50 && overlays.sma_50.length > 0) {
        traces.push({
            x: dates,
            y: overlays.sma_50,
            type: 'scatter',
            mode: 'lines',
            name: 'SMA 50',
            line: { color: '#F59E0B', width: 1.5 },
            yaxis: 'y'
        });
    }

    // 4. Bollinger Bands (Upper, Lower, Fill)
    if (overlays.bb_upper && overlays.bb_lower) {
        traces.push({
            x: dates,
            y: overlays.bb_upper,
            type: 'scatter',
            mode: 'lines',
            name: 'BB Upper',
            line: { color: '#CBD5E1', width: 1, dash: 'dot' },
            showlegend: false,
            yaxis: 'y'
        });
        traces.push({
            x: dates,
            y: overlays.bb_lower,
            type: 'scatter',
            mode: 'lines',
            name: 'BB Lower',
            line: { color: '#CBD5E1', width: 1, dash: 'dot' },
            fill: 'tonexty',
            fillcolor: 'rgba(226, 232, 240, 0.25)',
            showlegend: false,
            yaxis: 'y'
        });
    }

    // 5. Volume Subplot Bars
    traces.push({
        x: dates,
        y: payload.volume,
        type: 'bar',
        name: 'Volume',
        marker: { color: 'rgba(148, 163, 184, 0.35)' },
        yaxis: 'y2',
        showlegend: false
    });

    // 6. ML Forecast Trajectory and Uncertainty Cone
    if (forecast && forecast.dates && forecast.dates.length > 0) {
        // Lower uncertainty bound
        traces.push({
            x: forecast.dates,
            y: forecast.lower_bounds,
            type: 'scatter',
            mode: 'lines',
            name: 'Uncertainty Band',
            line: { color: 'rgba(59, 130, 246, 0.2)', width: 1, dash: 'dash' },
            showlegend: false,
            yaxis: 'y'
        });

        // Upper uncertainty bound with fill
        traces.push({
            x: forecast.dates,
            y: forecast.upper_bounds,
            type: 'scatter',
            mode: 'lines',
            name: '80% Confidence Cone',
            fill: 'tonexty',
            fillcolor: 'rgba(59, 130, 246, 0.08)',
            line: { color: 'rgba(59, 130, 246, 0.2)', width: 1, dash: 'dash' },
            yaxis: 'y'
        });

        // Projected Trajectory Mean Line
        const trajColor = forecast.direction === 'UP' ? '#10B981' : (forecast.direction === 'DOWN' ? '#EF4444' : '#64748B');
        traces.push({
            x: forecast.dates,
            y: forecast.prices,
            type: 'scatter',
            mode: 'lines+markers',
            name: `AI Forecast (${forecast.direction})`,
            line: { color: trajColor, width: 2.5, dash: 'solid' },
            marker: { size: 4, color: trajColor },
            yaxis: 'y'
        });
    }

    const layout = {
        dragmode: 'zoom',
        showlegend: true,
        legend: { orientation: 'h', y: 1.08, x: 0.01, font: { family: 'Inter', size: 11 } },
        margin: { l: 45, r: 20, t: 30, b: 30 },
        plot_bgcolor: '#FFFFFF',
        paper_bgcolor: '#FFFFFF',
        xaxis: {
            rangeslider: { visible: false },
            type: 'date',
            gridcolor: '#F1F5F9',
            linecolor: '#E2E8F0',
            tickfont: { family: 'Inter', size: 10, color: '#64748B' }
        },
        yaxis: {
            domain: [0.22, 1.0],
            gridcolor: '#F1F5F9',
            linecolor: '#E2E8F0',
            tickfont: { family: 'JetBrains Mono', size: 11, color: '#64748B' },
            tickprefix: quote.currency_symbol || ''
        },
        yaxis2: {
            domain: [0.0, 0.18],
            gridcolor: '#F8FAFC',
            showticklabels: false
        }
    };

    const config = {
        responsive: true,
        displayModeBar: true,
        displaylogo: false,
        modeBarButtonsToRemove: ['lasso2d', 'select2d']
    };

    Plotly.newPlot(el, traces, layout, config);
    state.chartInstances[elementId] = { payload, quote, layout };
}

// Timeframe Switcher on Existing Chart
function setupChartTimeframeButtons(chartId, symbol) {
    const group = document.getElementById(`tf-group-${chartId}`);
    if (!group) return;

    const btns = group.querySelectorAll(".tf-btn");
    btns.forEach(btn => {
        btn.addEventListener("click", async () => {
            btns.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            const tf = btn.getAttribute("data-tf");
            state.activeTimeframe = tf;

            // Fetch new timeframe data
            try {
                const res = await fetch(`/api/stock/${symbol}?timeframe=${tf}`);
                if (!res.ok) return;
                const fresh = await res.json();
                renderPlotlyChart(chartId, fresh.chart_payload, fresh.quote);
            } catch (e) {
                console.error("Timeframe update error:", e);
            }
        });
    });
}

// Render Normalized Comparison Chart
function renderComparisonPlotlyChart(elementId, comparison) {
    const el = document.getElementById(elementId);
    if (!el || !window.Plotly) return;

    const data = comparison.chart_data;
    const a = comparison.stock_a;
    const b = comparison.stock_b;

    const traces = [
        {
            x: data.dates,
            y: data.normalized_a,
            type: 'scatter',
            mode: 'lines',
            name: `${a.name} (${a.symbol})`,
            line: { color: '#2563EB', width: 2 }
        },
        {
            x: data.dates,
            y: data.normalized_b,
            type: 'scatter',
            mode: 'lines',
            name: `${b.name} (${b.symbol})`,
            line: { color: '#10B981', width: 2 }
        }
    ];

    const layout = {
        showlegend: true,
        legend: { orientation: 'h', y: 1.1, x: 0.01 },
        margin: { l: 45, r: 20, t: 25, b: 30 },
        plot_bgcolor: '#FFFFFF',
        paper_bgcolor: '#FFFFFF',
        xaxis: { gridcolor: '#F1F5F9', type: 'date' },
        yaxis: {
            gridcolor: '#F1F5F9',
            title: 'Base 100 Return',
            tickfont: { family: 'JetBrains Mono', size: 11 }
        }
    };

    Plotly.newPlot(el, traces, layout, { responsive: true, displaylogo: false });
}

// Helpers
function scrollToBottom() {
    const vp = document.getElementById("chat-viewport");
    setTimeout(() => {
        vp.scrollTop = vp.scrollHeight;
    }, 60);
}

function escapeHtml(str) {
    if (!str) return "";
    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// =========================================================================
// Companies Catalog Management
// =========================================================================
async function fetchCompaniesCatalog() {
    try {
        const res = await fetch("/api/companies");
        if (!res.ok) return;
        const data = await res.json();
        state.companies = data.companies || [];

        // Build category groupings
        state.categories = {};
        state.companies.forEach(c => {
            const cat = c.category || "Other";
            if (!state.categories[cat]) state.categories[cat] = [];
            state.categories[cat].push(c);
        });

        // Initial render in modal
        renderCompaniesGrid(state.companies);
    } catch (err) {
        console.error("Failed to load companies catalog:", err);
    }
}

// =========================================================================
// Companies Directory Modal Logic
// =========================================================================
function setupCompaniesModalHandlers() {
    if (!companiesModal) return;

    const openModal = () => {
        companiesModal.style.display = "flex";
        if (companyModalSearchInput) {
            companyModalSearchInput.value = "";
            companyModalSearchInput.focus();
        }
        state.activeModalCategory = "all";
        updateModalTabs("all");
        renderCompaniesGrid(state.companies);
    };

    const closeModal = () => {
        companiesModal.style.display = "none";
    };

    if (companiesModalBtn) companiesModalBtn.addEventListener("click", openModal);
    if (browseCompaniesBtn) browseCompaniesBtn.addEventListener("click", openModal);
    if (closeCompaniesModalBtn) closeCompaniesModalBtn.addEventListener("click", closeModal);

    // Close on clicking backdrop
    companiesModal.addEventListener("click", (e) => {
        if (e.target === companiesModal) closeModal();
    });

    // Modal search input
    if (companyModalSearchInput) {
        companyModalSearchInput.addEventListener("input", (e) => {
            const q = e.target.value.trim().toLowerCase();
            filterAndRenderModalCompanies(q, state.activeModalCategory);
        });
    }

    // Modal category tabs
    if (modalCategoryTabs) {
        modalCategoryTabs.querySelectorAll(".modal-tab-btn").forEach(tab => {
            tab.addEventListener("click", () => {
                const cat = tab.getAttribute("data-cat");
                state.activeModalCategory = cat;
                updateModalTabs(cat);
                const q = companyModalSearchInput ? companyModalSearchInput.value.trim().toLowerCase() : "";
                filterAndRenderModalCompanies(q, cat);
            });
        });
    }
}

function updateModalTabs(selectedCat) {
    if (!modalCategoryTabs) return;
    modalCategoryTabs.querySelectorAll(".modal-tab-btn").forEach(t => {
        if (t.getAttribute("data-cat") === selectedCat) {
            t.classList.add("active");
        } else {
            t.classList.remove("active");
        }
    });
}

function filterAndRenderModalCompanies(query, category) {
    let list = state.companies;

    // Filter by category
    if (category && category !== "all") {
        list = list.filter(c => c.category === category);
    }

    // Filter by query
    if (query) {
        list = list.filter(c => {
            const n = c.name.toLowerCase();
            const t = c.ticker.toLowerCase();
            const s = c.sector.toLowerCase();
            const a = (c.aliases || []).map(x => x.toLowerCase());
            return n.includes(query) || t.includes(query) || s.includes(query) || a.some(x => x.includes(query));
        });
    }

    renderCompaniesGrid(list);
}

function renderCompaniesGrid(companiesList) {
    if (!companiesGridContainer) return;
    companiesGridContainer.innerHTML = "";

    if (!companiesList || companiesList.length === 0) {
        companiesGridContainer.innerHTML = `
            <div style="grid-column: 1/-1; text-align: center; padding: 40px; color: var(--text-muted); font-size: 14px;">
                No companies found matching your search. Try another name or ticker.
            </div>
        `;
        return;
    }

    companiesList.forEach(comp => {
        const card = document.createElement("div");
        card.className = "company-card";
        card.innerHTML = `
            <div>
                <div class="cc-top">
                    <div class="cc-identity">
                        <span class="cc-emoji">${comp.emoji || '📈'}</span>
                        <span class="cc-name">${escapeHtml(comp.name)}</span>
                    </div>
                    <span class="cc-ticker-badge">${escapeHtml(comp.ticker)}</span>
                </div>
                <div class="cc-meta">
                    <span>${escapeHtml(comp.sector)}</span> • 
                    <span>${comp.exchange}</span>
                </div>
            </div>
            <div class="cc-actions">
                <button type="button" class="cc-analyze-btn" title="Analyze ${comp.name}">Analyze</button>
            </div>
        `;

        card.querySelector(".cc-analyze-btn").addEventListener("click", (e) => {
            e.stopPropagation();
            companiesModal.style.display = "none";
            userInput.value = `Analyze ${comp.name}`;
            submitUserQuery();
        });

        card.addEventListener("click", () => {
            companiesModal.style.display = "none";
            userInput.value = `Analyze ${comp.name}`;
            submitUserQuery();
        });

        companiesGridContainer.appendChild(card);
    });
}

// =========================================================================
// Real-time Chatbox Autocomplete Typeahead
// =========================================================================
function setupAutocompleteHandlers() {
    if (!userInput || !chatboxAutocomplete) return;

    userInput.addEventListener("input", (e) => {
        const val = userInput.value;
        const words = val.trim().split(/\s+/);
        const lastWord = words[words.length - 1];

        // Search if last word or entire input looks like a ticker/company
        const query = (words.length <= 3 ? val : lastWord).trim().toLowerCase();

        if (query.length < 2) {
            hideAutocomplete();
            return;
        }

        const matches = state.companies.filter(c => {
            const t = c.ticker.toLowerCase();
            const n = c.name.toLowerCase();
            const aliases = (c.aliases || []).map(a => a.toLowerCase());
            return t.startsWith(query) || n.startsWith(query) || t.includes(query) || n.includes(query) || aliases.some(a => a.startsWith(query) || a.includes(query));
        }).slice(0, 7);

        if (matches.length > 0) {
            renderAutocomplete(matches);
        } else {
            hideAutocomplete();
        }
    });

    // Keyboard navigation in autocomplete
    userInput.addEventListener("keydown", (e) => {
        if (chatboxAutocomplete.style.display === "none") return;

        const items = chatboxAutocomplete.querySelectorAll(".autocomplete-item");
        if (!items || items.length === 0) return;

        if (e.key === "ArrowDown") {
            e.preventDefault();
            state.selectedAutocompleteIndex = (state.selectedAutocompleteIndex + 1) % items.length;
            highlightAutocompleteItem(items);
        } else if (e.key === "ArrowUp") {
            e.preventDefault();
            state.selectedAutocompleteIndex = (state.selectedAutocompleteIndex - 1 + items.length) % items.length;
            highlightAutocompleteItem(items);
        } else if (e.key === "Enter" && state.selectedAutocompleteIndex >= 0) {
            e.preventDefault();
            items[state.selectedAutocompleteIndex].click();
        } else if (e.key === "Escape") {
            hideAutocomplete();
        }
    });

    // Close on click outside
    document.addEventListener("click", (e) => {
        if (!chatboxAutocomplete.contains(e.target) && e.target !== userInput) {
            hideAutocomplete();
        }
    });
}

function renderAutocomplete(matches) {
    chatboxAutocomplete.innerHTML = "";
    state.selectedAutocompleteIndex = -1;

    matches.forEach((comp, idx) => {
        const item = document.createElement("div");
        item.className = "autocomplete-item";
        item.innerHTML = `
            <div class="ac-left">
                <span class="ac-emoji">${comp.emoji || '📈'}</span>
                <div class="ac-names">
                    <span class="ac-title">${escapeHtml(comp.name)}</span>
                    <span class="ac-sub">${escapeHtml(comp.sector)}</span>
                </div>
            </div>
            <div class="ac-right">
                <span class="ac-ticker-pill">${escapeHtml(comp.ticker)}</span>
                <span class="ac-exch-pill">${comp.exchange}</span>
            </div>
        `;

        item.addEventListener("click", () => {
            selectAutocompleteCompany(comp);
        });

        chatboxAutocomplete.appendChild(item);
    });

    chatboxAutocomplete.style.display = "block";
}

function highlightAutocompleteItem(items) {
    items.forEach((it, idx) => {
        if (idx === state.selectedAutocompleteIndex) {
            it.classList.add("active");
            it.scrollIntoView({ block: "nearest" });
        } else {
            it.classList.remove("active");
        }
    });
}

function selectAutocompleteCompany(comp) {
    hideAutocomplete();
    const current = userInput.value.trim();
    if (current.toLowerCase().startsWith("analyze ") || current.toLowerCase().startsWith("compare ")) {
        const words = current.split(/\s+/);
        words[words.length - 1] = comp.name;
        userInput.value = words.join(" ");
    } else {
        userInput.value = `Analyze ${comp.name}`;
    }
    submitUserQuery();
}

function hideAutocomplete() {
    chatboxAutocomplete.style.display = "none";
    state.selectedAutocompleteIndex = -1;
}

// =========================================================================
// Welcome Screen Category Tabs Filter
// =========================================================================
function setupWelcomeCategoryFilter() {
    if (!welcomeCategoriesBar || !welcomeChipsContainer) return;

    welcomeCategoriesBar.querySelectorAll(".cat-pill").forEach(pill => {
        pill.addEventListener("click", () => {
            welcomeCategoriesBar.querySelectorAll(".cat-pill").forEach(p => p.classList.remove("active"));
            pill.classList.add("active");

            const cat = pill.getAttribute("data-cat");
            renderWelcomeCategoryChips(cat);
        });
    });
}

function renderWelcomeCategoryChips(category) {
    if (!welcomeChipsContainer) return;
    welcomeChipsContainer.innerHTML = "";

    let chipsToShow = [];
    if (category === "all") {
        chipsToShow = state.companies.filter(c => c.is_popular).slice(0, 14);
    } else {
        chipsToShow = state.companies.filter(c => c.category === category).slice(0, 14);
    }

    if (chipsToShow.length === 0) {
        chipsToShow = state.companies.slice(0, 12);
    }

    chipsToShow.forEach(c => {
        const chip = document.createElement("button");
        chip.className = "chip";
        chip.setAttribute("data-query", `Analyze ${c.name}.`);
        chip.innerHTML = `
            <span class="chip-icon">${c.emoji || '📈'}</span> ${escapeHtml(c.name)} <span class="chip-badge">${c.ticker}</span>
        `;
        chip.addEventListener("click", () => {
            userInput.value = `Analyze ${c.name}.`;
            submitUserQuery();
        });
        welcomeChipsContainer.appendChild(chip);
    });

    // Add generic market chips
    const mktChip = document.createElement("button");
    mktChip.className = "chip";
    mktChip.setAttribute("data-query", "How is the stock market today?");
    mktChip.innerHTML = `<span class="chip-icon">🌐</span> How is the market today?`;
    mktChip.addEventListener("click", () => {
        userInput.value = "How is the stock market today?";
        submitUserQuery();
    });
    welcomeChipsContainer.appendChild(mktChip);
}

// =========================================================================
// Library System: LocalStorage Past Conversations
// =========================================================================
const LIBRARY_STORAGE_KEY = "stockmind_conversations_v1";

function getLibraryData() {
    try {
        return JSON.parse(localStorage.getItem(LIBRARY_STORAGE_KEY) || "[]");
    } catch {
        return [];
    }
}

function saveToLibrary(userQuery, assistantData) {
    try {
        let library = getLibraryData();
        let conv = library.find(c => c.id === state.currentChatId);
        if (!conv) {
            conv = {
                id: state.currentChatId,
                title: userQuery.substring(0, 36) + (userQuery.length > 36 ? "…" : ""),
                symbol: state.activeSymbol,
                timestamp: Date.now(),
                dateStr: new Date().toLocaleDateString(undefined, { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" }),
                turns: []
            };
            library.unshift(conv);
        }
        conv.turns.push({ query: userQuery, response: assistantData });
        conv.timestamp = Date.now();
        conv.symbol = state.activeSymbol;
        if (library.length > 60) library.pop();
        localStorage.setItem(LIBRARY_STORAGE_KEY, JSON.stringify(library));
        updateLibraryBadge();
    } catch (e) {
        console.warn("Error saving conversation:", e);
    }
}

function updateLibraryBadge() {
    const library = getLibraryData();
    let badge = document.getElementById("library-count-badge");
    if (!badge && libraryBtn) {
        badge = document.createElement("span");
        badge.id = "library-count-badge";
        badge.className = "nav-badge";
        libraryBtn.appendChild(badge);
    }
    if (badge) {
        if (library.length > 0) {
            badge.textContent = library.length > 99 ? "99+" : library.length;
            badge.style.display = "inline-flex";
        } else {
            badge.style.display = "none";
        }
    }
}

function setupLibraryHandlers() {
    if (!libraryBtn || !libraryModal) return;

    libraryBtn.addEventListener("click", () => {
        renderLibraryList();
        libraryModal.style.display = "flex";
        if (librarySearchInput) librarySearchInput.value = "";
    });

    if (libraryCloseBtn) {
        libraryCloseBtn.addEventListener("click", () => {
            libraryModal.style.display = "none";
        });
    }

    libraryModal.addEventListener("click", (e) => {
        if (e.target === libraryModal) {
            libraryModal.style.display = "none";
        }
    });

    if (libraryClearAllBtn) {
        libraryClearAllBtn.addEventListener("click", () => {
            if (confirm("Clear all saved conversations from the library?")) {
                localStorage.removeItem(LIBRARY_STORAGE_KEY);
                renderLibraryList();
                updateLibraryBadge();
            }
        });
    }

    if (librarySearchInput) {
        librarySearchInput.addEventListener("input", (e) => {
            renderLibraryList(e.target.value.trim().toLowerCase());
        });
    }
}

function renderLibraryList(filterText = "") {
    if (!libraryListContainer) return;
    const library = getLibraryData();
    libraryListContainer.innerHTML = "";

    const filtered = filterText 
        ? library.filter(c => c.title.toLowerCase().includes(filterText) || (c.symbol && c.symbol.toLowerCase().includes(filterText)))
        : library;

    if (filtered.length === 0) {
        libraryListContainer.innerHTML = `
            <div class="library-empty-state">
                <div class="empty-icon">📂</div>
                <h4>${filterText ? "No matching conversations found" : "No saved conversations yet"}</h4>
                <p>Your stock analyses and queries will be automatically saved here as you chat.</p>
            </div>
        `;
        return;
    }

    filtered.forEach(conv => {
        const item = document.createElement("div");
        item.className = "library-item-card";
        const turnsCount = conv.turns ? conv.turns.length : 1;
        item.innerHTML = `
            <div class="library-item-main">
                <div class="library-item-header">
                    <span class="library-item-sym">${escapeHtml(conv.symbol || "STK")}</span>
                    <span class="library-item-date">${escapeHtml(conv.dateStr || "Recently")}</span>
                    <span class="library-item-turns">${turnsCount} ${turnsCount === 1 ? 'query' : 'queries'}</span>
                </div>
                <div class="library-item-title">${escapeHtml(conv.title)}</div>
            </div>
            <div class="library-item-actions">
                <button type="button" class="library-resume-btn" title="Open this conversation">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                    <span>Open</span>
                </button>
                <button type="button" class="library-del-btn" title="Delete conversation">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
                </button>
            </div>
        `;

        item.querySelector(".library-resume-btn").addEventListener("click", () => {
            loadConversationFromLibrary(conv.id);
        });

        item.querySelector(".library-del-btn").addEventListener("click", (e) => {
            e.stopPropagation();
            deleteFromLibrary(conv.id);
        });

        item.addEventListener("click", (e) => {
            if (!e.target.closest(".library-del-btn")) {
                loadConversationFromLibrary(conv.id);
            }
        });

        libraryListContainer.appendChild(item);
    });
}

function loadConversationFromLibrary(id) {
    const library = getLibraryData();
    const conv = library.find(c => c.id === id);
    if (!conv) return;

    stopSpeaking();
    messageList.innerHTML = "";
    welcomeScreen.style.display = "none";
    state.activeSymbol = conv.symbol || "TCS.NS";
    state.currentChatId = conv.id;

    if (conv.turns && conv.turns.length > 0) {
        conv.turns.forEach(turn => {
            appendUserMessage(turn.query);
            renderAssistantResponse(turn.response);
        });
    }

    if (libraryModal) libraryModal.style.display = "none";
}

function deleteFromLibrary(id) {
    let library = getLibraryData();
    library = library.filter(c => c.id !== id);
    localStorage.setItem(LIBRARY_STORAGE_KEY, JSON.stringify(library));
    renderLibraryList(librarySearchInput ? librarySearchInput.value.trim().toLowerCase() : "");
    updateLibraryBadge();
}
