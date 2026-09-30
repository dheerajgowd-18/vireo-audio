/**
 * Vireo Audio Support Intelligence Dashboard
 * Pure Vanilla JavaScript Application (Zero External Dependencies)
 */

(function () {
  'use strict';

  // Global Application State
  const appState = {
    currentView: 'overview',
    data: {
      overview: null,
      agents: null,
      trends: null,
      replacements: null,
      sla: null,
      ai: null,
      methodology: null,
    },
    agentsSort: { column: 'name', asc: true },
    agentsFilter: {
      tier: 'all',
      team: 'all',
      site: 'all',
      shift: 'all',
      minCsat: 0,
      search: '',
    },
    activeAgent: null,
  };

  // View Title Mapping
  const viewTitles = {
    overview: 'Support Intelligence',
    agents: 'Agent Performance',
    bottom10: 'Requested Bottom 10',
    ai: 'Ticket Intelligence',
    replacements: 'Replacement Risk',
    sla: 'Service Levels & Cost',
    methodology: 'Methodology & Data Quality',
  };

  // =========================================================================
  // Data Loaders
  // =========================================================================

  async function fetchJson(endpoint) {
    try {
      const response = await fetch(`data/${endpoint}.json`);
      if (!response.ok) {
        throw new Error(`HTTP error ${response.status} loading ${endpoint}.json`);
      }
      return await response.json();
    } catch (err) {
      console.error(`Failed to load ${endpoint}.json:`, err);
      return null;
    }
  }

  async function initData() {
    const [overview, agents, trends, replacements, sla, ai, methodology] = await Promise.all([
      fetchJson('overview'),
      fetchJson('agents'),
      fetchJson('trends'),
      fetchJson('replacements'),
      fetchJson('sla'),
      fetchJson('ai_signals'),
      fetchJson('methodology'),
    ]);

    appState.data.overview = overview;
    appState.data.agents = agents;
    appState.data.trends = trends;
    appState.data.replacements = replacements;
    appState.data.sla = sla;
    appState.data.ai = ai;
    appState.data.methodology = methodology;

    if (!overview || !agents) {
      showErrorState('Failed to load analytical data. Please verify web/data/ JSON files exist.');
      return;
    }

    renderCurrentView();
    setupEventListeners();
    populateFilterDropdowns();
  }

  function showErrorState(msg) {
    const container = document.querySelector('.content-container');
    container.innerHTML = `
      <div class="banner banner-danger" style="margin-top: 40px;">
        <span class="banner-icon">✕</span>
        <div>
          <strong>Data Loading Error:</strong> ${msg}
          <div style="margin-top: 8px; font-size: 11px;">
            Run <code>python scripts/build_web_data.py</code> to compile analytical JSON files.
          </div>
        </div>
      </div>
    `;
  }

  // =========================================================================
  // Navigation & Router
  // =========================================================================

  function navigateTo(viewId) {
    if (!viewTitles[viewId]) viewId = 'overview';
    appState.currentView = viewId;

    // Update Sidebar Navigation
    document.querySelectorAll('.nav-link').forEach((link) => {
      if (link.dataset.view === viewId) {
        link.classList.add('active');
      } else {
        link.classList.remove('active');
      }
    });

    // Update Page Header
    const titleEl = document.getElementById('page-title');
    if (titleEl) titleEl.textContent = viewTitles[viewId];

    // Toggle Section Views
    document.querySelectorAll('.page-view').forEach((sec) => {
      sec.classList.remove('active');
    });
    const targetSection = document.getElementById(`view-${viewId}`);
    if (targetSection) {
      targetSection.classList.add('active');
    }

    renderCurrentView();
  }

  function renderCurrentView() {
    const view = appState.currentView;
    if (view === 'overview') renderOverviewView();
    else if (view === 'agents') renderAgentsView();
    else if (view === 'bottom10') renderBottom10View();
    else if (view === 'ai') renderAIView();
    else if (view === 'replacements') renderReplacementsView();
    else if (view === 'sla') renderSLAView();
  }

  // =========================================================================
  // View 1: Overview
  // =========================================================================

  function renderOverviewView() {
    const data = appState.data.overview;
    if (!data) return;

    // Populate KPIs
    document.getElementById('kpi-csat').textContent = data.kpis.csat.value;
    document.getElementById('kpi-csat-sub').textContent = data.kpis.csat.subtext;

    document.getElementById('kpi-handle').textContent = data.kpis.median_handle_time.value;
    document.getElementById('kpi-handle-sub').textContent = data.kpis.median_handle_time.subtext;

    document.getElementById('kpi-sla').textContent = data.kpis.sla_breach_rate.value;
    document.getElementById('kpi-sla-sub').textContent = data.kpis.sla_breach_rate.subtext;

    document.getElementById('kpi-repl-units').textContent = data.kpis.replacement_units.value;
    document.getElementById('kpi-repl-units-sub').textContent = data.kpis.replacement_units.subtext;

    document.getElementById('kpi-repl-spend').textContent = data.kpis.replacement_spend.value;
    document.getElementById('kpi-repl-spend-sub').textContent = data.kpis.replacement_spend.subtext;

    document.getElementById('kpi-sla-credits').textContent = data.kpis.sla_credit_exposure.value;
    document.getElementById('kpi-sla-credits-sub').textContent = data.kpis.sla_credit_exposure.subtext;

    // Render 18-Month Dual Line Chart
    renderTrendLineChart('overview-trend-chart', data.monthly_trend);

    // Render Key Signal Cards
    const signalsEl = document.getElementById('overview-signals');
    if (signalsEl && signalsEl.children.length === 0) {
      signalsEl.innerHTML = data.key_signals
        .map(
          (sig) => `
        <div class="signal-card">
          <div class="signal-card-header">
            <span class="signal-title">${sig.title}</span>
            <span class="badge badge-${sig.badge_type}">${sig.badge}</span>
          </div>
          <div class="signal-metric">${sig.metric}</div>
          <div class="signal-evidence">${sig.evidence}</div>
          <div class="signal-interpretation">${sig.interpretation}</div>
        </div>
      `
        )
        .join('');
    }
  }

  // =========================================================================
  // View 2: Agent Performance Table & Filters
  // =========================================================================

  function populateFilterDropdowns() {
    const agentsData = appState.data.agents;
    if (!agentsData || !agentsData.filters) return;

    const teamSelect = document.getElementById('agent-filter-team');
    agentsData.filters.teams.forEach((t) => {
      const opt = document.createElement('option');
      opt.value = t;
      opt.textContent = t;
      teamSelect.appendChild(opt);
    });

    const siteSelect = document.getElementById('agent-filter-site');
    agentsData.filters.sites.forEach((s) => {
      const opt = document.createElement('option');
      opt.value = s;
      opt.textContent = s;
      siteSelect.appendChild(opt);
    });

    const shiftSelect = document.getElementById('agent-filter-shift');
    agentsData.filters.shifts.forEach((sh) => {
      const opt = document.createElement('option');
      opt.value = sh;
      opt.textContent = sh;
      shiftSelect.appendChild(opt);
    });
  }

  function getFilteredAgents() {
    const agentsData = appState.data.agents;
    if (!agentsData) return [];

    let list = [...agentsData.agents];
    const f = appState.agentsFilter;

    if (f.tier !== 'all') {
      list = list.filter((a) => a.tier === parseInt(f.tier, 10));
    }
    if (f.team !== 'all') {
      list = list.filter((a) => a.team === f.team);
    }
    if (f.site !== 'all') {
      list = list.filter((a) => a.site === f.site);
    }
    if (f.shift !== 'all') {
      list = list.filter((a) => a.shift === f.shift);
    }
    if (f.minCsat > 0) {
      list = list.filter((a) => a.csat_n >= f.minCsat);
    }
    if (f.search.trim()) {
      const q = f.search.toLowerCase().trim();
      list = list.filter(
        (a) =>
          a.name.toLowerCase().includes(q) ||
          a.agent_id.toLowerCase().includes(q) ||
          a.team.toLowerCase().includes(q)
      );
    }

    // Sort
    const col = appState.agentsSort.column;
    const asc = appState.agentsSort.asc;
    list.sort((a, b) => {
      let valA = a[col];
      let valB = b[col];

      if (valA === null || valA === undefined) valA = asc ? Infinity : -Infinity;
      if (valB === null || valB === undefined) valB = asc ? Infinity : -Infinity;

      if (typeof valA === 'string') {
        return asc ? valA.localeCompare(valB) : valB.localeCompare(valA);
      }
      return asc ? valA - valB : valB - valA;
    });

    return list;
  }

  function renderAgentsView() {
    const list = getFilteredAgents();
    const countEl = document.getElementById('agent-table-count');
    if (countEl) countEl.textContent = `Showing ${list.length} of 44 Agents`;

    const tbody = document.getElementById('agents-table-body');
    if (!tbody) return;

    tbody.innerHTML = list
      .map((a) => {
        let roleBadge = '';
        if (a.is_hardware_triage) {
          roleBadge = '<span class="badge badge-warning" style="margin-left: 6px;">Hardware Triage</span>';
        } else if (a.tier === 2) {
          roleBadge = '<span class="badge badge-accent" style="margin-left: 6px;">Tier 2</span>';
        }

        const csatStr = a.mean_csat !== null ? a.mean_csat.toFixed(2) : '-';
        return `
        <tr class="clickable-row" data-agent-id="${a.agent_id}">
          <td>
            <strong>${a.name}</strong> <span style="font-size: 11px; color: var(--text-subtle);">(${a.agent_id})</span>
            ${roleBadge}
          </td>
          <td>${a.team}</td>
          <td>Tier ${a.tier}</td>
          <td class="table-cell-num">${a.tickets.toLocaleString()}</td>
          <td class="table-cell-num" style="font-weight: 600;">${csatStr}</td>
          <td class="table-cell-num">${a.csat_n}</td>
          <td class="table-cell-num">${a.median_handle_minutes.toFixed(0)}m</td>
          <td class="table-cell-num">${a.sla_breach_rate_pct.toFixed(1)}%</td>
          <td class="table-cell-num">${a.transfers}</td>
          <td class="table-cell-num">${a.replacements}</td>
        </tr>
      `;
      })
      .join('');

    // Attach row click listeners for detail drawer
    tbody.querySelectorAll('tr').forEach((row) => {
      row.addEventListener('click', () => {
        const agentId = row.dataset.agentId;
        openAgentDrawer(agentId);
      });
    });
  }

  // =========================================================================
  // View 3: Requested Bottom 10
  // =========================================================================

  function renderBottom10View() {
    const data = appState.data.agents;
    if (!data || !data.bottom_10) return;

    const b10 = data.bottom_10;
    const tbody = document.getElementById('bottom10-table-body');
    if (!tbody) return;

    tbody.innerHTML = b10.agents
      .map(
        (a) => `
      <tr class="clickable-row" data-agent-id="${a.agent_id}">
        <td class="num" style="font-weight: 700;">#${a.raw_rank}</td>
        <td><code>${a.agent_id}</code></td>
        <td><strong>${a.name}</strong></td>
        <td>${a.team}</td>
        <td>Tier ${a.tier}</td>
        <td class="table-cell-num">${a.tickets}</td>
        <td class="table-cell-num">${a.csat_n}</td>
        <td class="table-cell-num" style="font-weight: 700; color: var(--danger);">${a.mean_csat.toFixed(2)}</td>
        <td class="table-cell-num">${a.median_handle_hours.toFixed(1)}h</td>
        <td>
          ${
            a.is_hardware_triage
              ? '<span class="badge badge-warning">Hardware Triage</span>'
              : a.tier === 2
              ? '<span class="badge badge-accent">Tier 2 Escalations</span>'
              : '<span class="badge badge-default">Standard</span>'
          }
        </td>
      </tr>
    `
      )
      .join('');

    // Attach row click listeners
    tbody.querySelectorAll('tr').forEach((row) => {
      row.addEventListener('click', () => {
        const agentId = row.dataset.agentId;
        openAgentDrawer(agentId);
      });
    });

    // Populate Breakdown Counters
    document.getElementById('b10-tier2-count').textContent = `${b10.composition.tier_2_count} / 10`;
    document.getElementById('b10-hw-count').textContent = `${b10.composition.hardware_triage_tier_1_count} / 10`;
    document.getElementById('b10-other-count').textContent = `${b10.composition.standard_tier_1_count} / 10`;
  }

  // =========================================================================
  // View 4: AI Signals
  // =========================================================================

  function renderAIView() {
    const data = appState.data.ai;
    if (!data) return;

    // Render Decomposition Horizontal Bars
    const container = document.getElementById('ai-category-bars');
    if (container && container.children.length === 0) {
      const items = data.other_decomposition.distribution.slice(0, 7);
      const maxVal = Math.max(...items.map((i) => i.count));

      container.innerHTML = items
        .map(
          (item) => `
        <div class="bar-row">
          <div class="bar-label" style="width: 140px;" title="${item.category}">${item.category}</div>
          <div class="bar-track">
            <div class="bar-fill ${item.category === 'other_unclear' ? 'bar-fill-warning' : ''}" 
                 style="width: ${(item.count / maxVal) * 100}%;"></div>
          </div>
          <div class="bar-value">${item.count} (${item.pct}%)</div>
        </div>
      `
        )
        .join('');
    }
  }

  // =========================================================================
  // View 5: Replacements
  // =========================================================================

  function renderReplacementsView() {
    const data = appState.data.replacements;
    if (!data) return;

    // Product Table
    const ptbody = document.getElementById('product-repl-tbody');
    if (ptbody && ptbody.children.length === 0) {
      ptbody.innerHTML = data.product_breakdown
        .map(
          (p) => `
        <tr ${p.sku === 'VA-EB-PL2' ? 'style="background-color: var(--surface-subtle); font-weight: 600;"' : ''}>
          <td><code>${p.sku}</code></td>
          <td>
            ${p.product_name}
            ${p.sku === 'VA-EB-PL2' ? '<span class="badge badge-danger" style="margin-left: 6px;">61.5% Replacements</span>' : ''}
          </td>
          <td class="table-cell-num">${p.tickets.toLocaleString()}</td>
          <td class="table-cell-num">${p.replacements.toLocaleString()}</td>
          <td class="table-cell-num">${p.replacement_rate_pct.toFixed(1)}%</td>
          <td class="table-cell-num num">${p.policy_spend_formatted}</td>
        </tr>
      `
        )
        .join('');
    }

    // Lot Investigation Table
    const ltbody = document.getElementById('lot-tbody');
    if (ltbody && ltbody.children.length === 0) {
      ltbody.innerHTML = data.lot_investigation.candidates
        .map(
          (l) => `
        <tr>
          <td><code>${l.lot_code}</code></td>
          <td><code>${l.product_sku}</code></td>
          <td class="table-cell-num">${l.orders}</td>
          <td class="table-cell-num">${l.tickets}</td>
          <td class="table-cell-num" style="font-weight: 600;">${l.replacements}</td>
          <td class="table-cell-num">${l.replacement_rate_pct.toFixed(1)}%</td>
          <td><span class="badge badge-warning">${l.candidate_status}</span></td>
        </tr>
      `
        )
        .join('');
    }
  }

  // =========================================================================
  // View 6: SLA & Cost
  // =========================================================================

  function renderSLAView() {
    const data = appState.data.sla;
    if (!data) return;

    // Channel Table
    const tbody = document.getElementById('sla-channel-tbody');
    if (tbody && tbody.children.length === 0) {
      tbody.innerHTML = data.channels
        .map(
          (c) => `
        <tr>
          <td><strong>${c.channel}</strong></td>
          <td class="table-cell-num">${c.tickets.toLocaleString()}</td>
          <td class="table-cell-num">${c.sla_target_minutes}m</td>
          <td class="table-cell-num">${c.breaches}</td>
          <td class="table-cell-num" style="font-weight: 600; color: ${c.breach_rate_pct > 10 ? 'var(--danger)' : 'var(--text)'};">
            ${c.breach_rate_pct.toFixed(2)}%
          </td>
          <td class="table-cell-num num">${c.credit_exposure_formatted}</td>
          <td class="table-cell-num num">${c.contact_cost_formatted}</td>
        </tr>
      `
        )
        .join('');
    }

    // Horizontal Breach Rate Bars
    const barContainer = document.getElementById('sla-breach-bars');
    if (barContainer && barContainer.children.length === 0) {
      const maxBreach = 15; // Max 15% scale
      barContainer.innerHTML = data.channels
        .map(
          (c) => `
        <div class="bar-row">
          <div class="bar-label">${c.channel}</div>
          <div class="bar-track">
            <div class="bar-fill ${c.breach_rate_pct > 10 ? 'bar-fill-danger' : ''}" 
                 style="width: ${(c.breach_rate_pct / maxBreach) * 100}%;"></div>
          </div>
          <div class="bar-value">${c.breach_rate_pct.toFixed(2)}% (${c.breaches})</div>
        </div>
      `
        )
        .join('');
    }
  }

  // =========================================================================
  // Native SVG Line Chart Renderer (Zero Chart Libraries)
  // =========================================================================

  function renderTrendLineChart(containerId, records) {
    const container = document.getElementById(containerId);
    if (!container || !records || records.length === 0) return;
    container.innerHTML = '';

    const width = container.clientWidth || 800;
    const height = 240;
    const padding = { top: 20, right: 30, bottom: 35, left: 50 };

    const plotW = width - padding.left - padding.right;
    const plotH = height - padding.top - padding.bottom;

    const maxTickets = Math.max(...records.map((r) => r.ticket_volume));
    const maxRepl = Math.max(...records.map((r) => r.replacement_count));

    // Scales
    const xScale = (idx) => padding.left + (idx / (records.length - 1)) * plotW;
    const yTickets = (val) => padding.top + plotH - (val / (maxTickets * 1.15)) * plotH;
    const yRepl = (val) => padding.top + plotH - (val / (maxRepl * 1.4)) * plotH;

    // SVG Element
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('viewBox', `0 0 ${width} ${height}`);
    svg.setAttribute('class', 'chart-svg');

    // Horizontal Gridlines
    const gridG = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    gridG.setAttribute('class', 'chart-grid');
    for (let step = 0; step <= 4; step++) {
      const y = padding.top + (step / 4) * plotH;
      const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
      line.setAttribute('x1', padding.left);
      line.setAttribute('x2', width - padding.right);
      line.setAttribute('y1', y);
      line.setAttribute('y2', y);
      gridG.appendChild(line);
    }
    svg.appendChild(gridG);

    // Build Paths
    let pathTicketsD = '';
    let pathReplD = '';
    records.forEach((r, idx) => {
      const x = xScale(idx);
      const yt = yTickets(r.ticket_volume);
      const yr = yRepl(r.replacement_count);

      pathTicketsD += `${idx === 0 ? 'M' : 'L'} ${x} ${yt} `;
      pathReplD += `${idx === 0 ? 'M' : 'L'} ${x} ${yr} `;
    });

    const pathT = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    pathT.setAttribute('d', pathTicketsD);
    pathT.setAttribute('class', 'chart-line chart-line-primary');
    svg.appendChild(pathT);

    const pathR = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    pathR.setAttribute('d', pathReplD);
    pathR.setAttribute('class', 'chart-line chart-line-secondary');
    svg.appendChild(pathR);

    // Tooltip Element
    let tooltip = container.querySelector('.chart-tooltip');
    if (!tooltip) {
      tooltip = document.createElement('div');
      tooltip.className = 'chart-tooltip';
      container.appendChild(tooltip);
    }

    // Points & Axis Labels
    const axisG = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    axisG.setAttribute('class', 'chart-axis');

    records.forEach((r, idx) => {
      const x = xScale(idx);

      // X-Axis Month Label (every 2 months)
      if (idx % 2 === 0 || idx === records.length - 1) {
        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.setAttribute('x', x);
        text.setAttribute('y', height - 10);
        text.setAttribute('text-anchor', 'middle');
        // format "2025-01" -> "Jan '25"
        const parts = r.month.split('-');
        const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        const mStr = monthNames[parseInt(parts[1], 10) - 1];
        text.textContent = `${mStr} '${parts[0].slice(2)}`;
        axisG.appendChild(text);
      }

      // Interactive Circle on Ticket line
      const pt = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      pt.setAttribute('cx', x);
      pt.setAttribute('cy', yTickets(r.ticket_volume));
      pt.setAttribute('r', 3);
      pt.setAttribute('class', 'chart-point chart-line-primary');
      pt.setAttribute('stroke', '#2563eb');

      pt.addEventListener('mouseenter', (e) => {
        tooltip.innerHTML = `
          <strong>${r.month}</strong><br>
          Tickets: <strong>${r.ticket_volume.toLocaleString()}</strong><br>
          Replacements: <strong>${r.replacement_count} (${r.replacement_rate_pct}%)</strong><br>
          Spend: <strong>₹${(r.policy_replacement_cost / 100000).toFixed(2)}L</strong>
        `;
        tooltip.style.display = 'block';
        tooltip.style.left = `${x - 40}px`;
        tooltip.style.top = `${yTickets(r.ticket_volume) - 60}px`;
      });

      pt.addEventListener('mouseleave', () => {
        tooltip.style.display = 'none';
      });

      svg.appendChild(pt);
    });

    svg.appendChild(axisG);
    container.appendChild(svg);
  }

  // =========================================================================
  // Agent Detail Flyout Drawer
  // =========================================================================

  function openAgentDrawer(agentId) {
    const agentsData = appState.data.agents;
    if (!agentsData) return;

    const agent = agentsData.agents.find((a) => a.agent_id === agentId);
    if (!agent) return;

    document.getElementById('drawer-agent-name').textContent = agent.name;
    document.getElementById('drawer-agent-id').textContent = `${agent.agent_id} · ${agent.benchmark_group}`;

    document.getElementById('drawer-team').textContent = agent.team;
    document.getElementById('drawer-tier').textContent = `Tier ${agent.tier}`;
    document.getElementById('drawer-site').textContent = agent.site;
    document.getElementById('drawer-shift').textContent = `${agent.shift} Shift`;

    const triageBadge = document.getElementById('drawer-triage-badge');
    if (agent.is_hardware_triage) {
      triageBadge.style.display = 'inline-block';
    } else {
      triageBadge.style.display = 'none';
    }

    document.getElementById('drawer-csat').textContent = agent.mean_csat !== null ? agent.mean_csat.toFixed(2) : 'N/A';
    document.getElementById('drawer-csat-n').textContent = `${agent.csat_n} (${agent.csat_response_rate_pct}% rate)`;
    document.getElementById('drawer-handle').textContent = `${agent.median_handle_minutes.toFixed(0)}m (mean: ${agent.mean_handle_hours.toFixed(1)}h)`;
    document.getElementById('drawer-sla').textContent = `${agent.sla_breach_rate_pct.toFixed(1)}% (${agent.sla_breaches} breaches)`;

    document.getElementById('drawer-top-cats').textContent = agent.details.top_issue_categories;
    document.getElementById('drawer-hw-count').textContent = `${agent.details.hw_defect_tickets} tickets`;
    document.getElementById('drawer-hw-pct').textContent = `${agent.details.hw_defect_share_pct.toFixed(1)}%`;
    document.getElementById('drawer-notes-count').textContent = `${agent.details.uninformative_notes} (${agent.details.uninformative_note_pct.toFixed(1)}%)`;
    document.getElementById('drawer-low-csat').textContent = `${agent.details.low_csat_tickets} tickets`;

    document.getElementById('drawer-overlay').classList.add('active');
    document.getElementById('agent-drawer').classList.add('active');
  }

  function closeAgentDrawer() {
    document.getElementById('drawer-overlay').classList.remove('active');
    document.getElementById('agent-drawer').classList.remove('active');
  }

  // =========================================================================
  // Event Listeners & Interaction Setup
  // =========================================================================

  function setupEventListeners() {
    // Hash Routing
    window.addEventListener('hashchange', () => {
      const hash = window.location.hash.replace('#', '') || 'overview';
      navigateTo(hash);
    });
    if (window.location.hash) {
      navigateTo(window.location.hash.replace('#', ''));
    }

    // Nav Click Handling
    document.querySelectorAll('.nav-link').forEach((link) => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const view = link.dataset.view;
        window.location.hash = `#${view}`;
        navigateTo(view);
      });
    });

    // Theme Toggle
    const themeBtn = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    themeBtn.addEventListener('click', () => {
      const html = document.documentElement;
      const current = html.getAttribute('data-theme') || 'light';
      const next = current === 'light' ? 'dark' : 'light';
      html.setAttribute('data-theme', next);
      themeIcon.textContent = next === 'dark' ? '☼' : '◐';
      localStorage.setItem('vireo-theme', next);
    });
    const savedTheme = localStorage.getItem('vireo-theme');
    if (savedTheme) {
      document.documentElement.setAttribute('data-theme', savedTheme);
      themeIcon.textContent = savedTheme === 'dark' ? '☼' : '◐';
    }

    // Table Header Sorting
    document.querySelectorAll('#agents-table th.sortable').forEach((th) => {
      th.addEventListener('click', () => {
        const col = th.dataset.sort;
        if (appState.agentsSort.column === col) {
          appState.agentsSort.asc = !appState.agentsSort.asc;
        } else {
          appState.agentsSort.column = col;
          appState.agentsSort.asc = true;
        }
        renderAgentsView();
      });
    });

    // Table Filters
    document.getElementById('agent-filter-tier').addEventListener('change', (e) => {
      appState.agentsFilter.tier = e.target.value;
      renderAgentsView();
    });
    document.getElementById('agent-filter-team').addEventListener('change', (e) => {
      appState.agentsFilter.team = e.target.value;
      renderAgentsView();
    });
    document.getElementById('agent-filter-site').addEventListener('change', (e) => {
      appState.agentsFilter.site = e.target.value;
      renderAgentsView();
    });
    document.getElementById('agent-filter-shift').addEventListener('change', (e) => {
      appState.agentsFilter.shift = e.target.value;
      renderAgentsView();
    });
    document.getElementById('agent-filter-min-csat').addEventListener('change', (e) => {
      appState.agentsFilter.minCsat = parseInt(e.target.value, 10);
      renderAgentsView();
    });

    // Global Search
    const searchInput = document.getElementById('global-search');
    searchInput.addEventListener('input', (e) => {
      appState.agentsFilter.search = e.target.value;
      if (appState.currentView !== 'agents') {
        window.location.hash = '#agents';
        navigateTo('agents');
      }
      renderAgentsView();
    });

    // Drawer Close Listeners
    document.getElementById('drawer-close-btn').addEventListener('click', closeAgentDrawer);
    document.getElementById('drawer-overlay').addEventListener('click', closeAgentDrawer);
    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeAgentDrawer();
    });
  }

  // Initialize Application on DOM Ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initData);
  } else {
    initData();
  }
})();
