// YouTube Watch History Analytics - Charts & Table Logic
// Geist System Monochromatic & Subtle Accent Palette for Charts
Chart.defaults.color = '#8f8f8f';
Chart.defaults.font.family = "'Geist', -apple-system, sans-serif";
Chart.defaults.borderColor = '#ebebeb';

// 1. Language Doughnut
new Chart(document.getElementById('chartLang'), {
  type: 'doughnut',
  data: {
    labels: langData.labels,
    datasets: [{
      data: langData.counts,
      backgroundColor: ['#171717', '#4d4d4d', '#737373', '#a1a1a1', '#d4d4d4', '#0070f3', '#7928ca'],
      borderWidth: 2,
      borderColor: '#ffffff'
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    cutout: '68%',
    plugins: {
      legend: {
        position: 'right',
        labels: { boxWidth: 12, usePointStyle: true, pointStyle: 'circle' }
      }
    }
  }
});

// 2. Top Channels Bar
new Chart(document.getElementById('chartChannels'), {
  type: 'bar',
  data: {
    labels: topChannelsData.labels,
    datasets: [{
      label: 'Views',
      data: topChannelsData.counts,
      backgroundColor: '#171717',
      borderRadius: 4
    }]
  },
  options: {
    indexAxis: 'y',
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { display: false } },
    scales: {
      x: { grid: { display: false } },
      y: { grid: { display: false } }
    }
  }
});

// 3. Genre Breakdown
new Chart(document.getElementById('chartGenre'), {
  type: 'bar',
  data: {
    labels: genreData.labels,
    datasets: [{
      label: 'Videos',
      data: genreData.counts,
      backgroundColor: '#171717',
      borderRadius: 4
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { display: false } },
    scales: {
      x: { 
        ticks: { maxRotation: 45, minRotation: 20 },
        grid: { display: false } 
      },
      y: { grid: { color: '#f2f2f2' } }
    }
  }
});

// 4. Hourly Activity (Smooth Line)
new Chart(document.getElementById('chartHourly'), {
  type: 'line',
  data: {
    labels: hourlyData.labels,
    datasets: [{
      label: 'Activity',
      data: hourlyData.counts,
      borderColor: '#171717',
      borderWidth: 2,
      backgroundColor: 'rgba(0, 0, 0, 0.03)',
      fill: true,
      tension: 0.35,
      pointRadius: 2.5,
      pointHoverRadius: 5
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { display: false } },
    scales: {
      x: { grid: { display: false } },
      y: { grid: { color: '#f2f2f2' } }
    }
  }
});

// 5. Day of Week Bar
new Chart(document.getElementById('chartDow'), {
  type: 'bar',
  data: {
    labels: dowData.labels,
    datasets: [{
      label: 'Views',
      data: dowData.counts,
      backgroundColor: '#4d4d4d',
      borderRadius: 4
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { display: false } },
    scales: {
      x: { grid: { display: false } },
      y: { grid: { color: '#f2f2f2' } }
    }
  }
});

// 6. Monthly Trajectory
new Chart(document.getElementById('chartTimeline'), {
  type: 'line',
  data: {
    labels: timelineData.labels,
    datasets: [{
      label: 'Monthly Videos',
      data: timelineData.counts,
      borderColor: '#0070f3',
      borderWidth: 2,
      backgroundColor: 'rgba(0, 112, 243, 0.04)',
      fill: true,
      tension: 0.3,
      pointRadius: 3.5,
      pointBackgroundColor: '#0070f3'
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { display: false } },
    scales: {
      x: { grid: { display: false } },
      y: { grid: { color: '#f2f2f2' } }
    }
  }
});

// Table Pagination & Filter Logic
let filteredData = [...rawData];
let currentPage = 1;
const pageSize = 50;

function applyFilters() {
  const query = document.getElementById('searchInput').value.toLowerCase();
  const lang = document.getElementById('langFilter').value;
  const genre = document.getElementById('genreFilter').value;

  filteredData = rawData.filter(item => {
    const matchesQuery = !query || 
      item.t.toLowerCase().includes(query) || 
      item.c.toLowerCase().includes(query) || 
      item.d.toLowerCase().includes(query);
    const matchesLang = !lang || item.l === lang;
    const matchesGenre = !genre || item.g === genre;
    return matchesQuery && matchesLang && matchesGenre;
  });

  currentPage = 1;
  renderTable();
}

function renderTable() {
  const tbody = document.getElementById('tableBody');
  tbody.innerHTML = '';

  const start = (currentPage - 1) * pageSize;
  const end = Math.min(start + pageSize, filteredData.length);
  const pageItems = filteredData.slice(start, end);

  if (pageItems.length === 0) {
    tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; padding: 32px; color: var(--mute); font-family: Geist Mono, monospace;">No matching records found.</td></tr>';
  } else {
    pageItems.forEach(item => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td><a href="${item.u}" target="_blank" class="table-video-title">${item.t}</a></td>
        <td>${item.c}</td>
        <td><span class="pill-tag">${item.g}</span></td>
        <td><span class="pill-tag">${item.l}</span></td>
        <td class="timestamp">${item.d}</td>
      `;
      tbody.appendChild(tr);
    });
  }

  document.getElementById('pageInfo').innerText = filteredData.length === 0 
    ? 'Showing 0 of 0 entries'
    : `Showing ${start + 1} to ${end} of ${filteredData.length.toLocaleString()} entries`;

  document.getElementById('prevBtn').disabled = currentPage === 1;
  document.getElementById('nextBtn').disabled = end >= filteredData.length;
}

function prevPage() {
  if (currentPage > 1) {
    currentPage--;
    renderTable();
  }
}

function nextPage() {
  if ((currentPage * pageSize) < filteredData.length) {
    currentPage++;
    renderTable();
  }
}

document.getElementById('searchInput').addEventListener('input', applyFilters);
document.getElementById('langFilter').addEventListener('change', applyFilters);
document.getElementById('genreFilter').addEventListener('change', applyFilters);

renderTable();
