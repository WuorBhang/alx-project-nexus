// Global variables
let authToken = localStorage.getItem('authToken');
let currentUser = JSON.parse(localStorage.getItem('currentUser'));

// DOM Elements
const apiBaseUrl = '/api';

// Helper Functions
function showAlert(message, type = 'danger') {
    const alertContainer = document.getElementById('alert-container');
    if (!alertContainer) return;
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.textContent = message;
    
    alertContainer.innerHTML = '';
    alertContainer.appendChild(alert);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        alert.remove();
    }, 5000);
}

function formatDate(dateString) {
    const options = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

function getStatusClass(status) {
    switch(status) {
        case 'Active':
            return 'status-active';
        case 'Ended':
            return 'status-ended';
        case 'Upcoming':
            return 'status-upcoming';
        default:
            return '';
    }
}

// API Functions
async function apiRequest(endpoint, method = 'GET', data = null) {
    const headers = {
        'Content-Type': 'application/json'
    };
    
    if (authToken) {
        headers['Authorization'] = `Token ${authToken}`;
    }
    
    const config = {
        method,
        headers,
        credentials: 'same-origin'
    };
    
    if (data && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
        config.body = JSON.stringify(data);
    }
    
    try {
        console.log(`Making ${method} request to: ${apiBaseUrl}${endpoint}`);
        const response = await fetch(`${apiBaseUrl}${endpoint}`, config);
        
        console.log(`Response status: ${response.status}`);
        
        if (response.status === 401) {
            // Unauthorized - clear token and redirect to login
            localStorage.removeItem('authToken');
            localStorage.removeItem('currentUser');
            authToken = null;
            currentUser = null;
            window.location.href = '/login.html';
            return null;
        }
        
        let result;
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            result = await response.json();
        } else {
            result = await response.text();
        }
        
        if (!response.ok) {
            let errorMessage = 'Something went wrong';
            if (result && typeof result === 'object') {
                if (result.error) {
                    errorMessage = result.error;
                } else if (result.detail) {
                    errorMessage = result.detail;
                } else if (result.non_field_errors) {
                    errorMessage = Array.isArray(result.non_field_errors) ? result.non_field_errors[0] : result.non_field_errors;
                } else {
                    // Handle field-specific errors
                    const fieldErrors = Object.values(result).flat();
                    if (fieldErrors.length > 0) {
                        errorMessage = fieldErrors[0];
                    }
                }
            } else if (typeof result === 'string') {
                errorMessage = result;
            }
            throw new Error(errorMessage);
        }
        
        return result;
    } catch (error) {
        console.error('API Error:', error);
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            showAlert('Network error: Unable to connect to the server. Please check your internet connection.');
        } else {
            showAlert(error.message || 'An unexpected error occurred');
        }
        return null;
    }
}

// Authentication Functions
async function registerUser(userData) {
    console.log('Registering user with data:', userData);
    const result = await apiRequest('/register/', 'POST', userData);
    if (result && result.token && result.user) {
        authToken = result.token;
        currentUser = result.user;
        
        localStorage.setItem('authToken', authToken);
        localStorage.setItem('currentUser', JSON.stringify(currentUser));
        
        console.log('Registration successful');
        return true;
    }
    console.log('Registration failed');
    return false;
}

async function loginUser(credentials) {
    const result = await apiRequest('/login/', 'POST', credentials);
    if (result) {
        authToken = result.token;
        currentUser = result.user;
        
        localStorage.setItem('authToken', authToken);
        localStorage.setItem('currentUser', JSON.stringify(currentUser));
        
        return true;
    }
    return false;
}

function logoutUser() {
    localStorage.removeItem('authToken');
    localStorage.removeItem('currentUser');
    authToken = null;
    currentUser = null;
    window.location.href = '/login.html';
}

// Poll Functions
async function getPolls() {
    return await apiRequest('/polls/');
}

async function getPollDetails(pollId) {
    return await apiRequest(`/polls/${pollId}/`);
}

async function getPollResults(pollId) {
    return await apiRequest(`/polls/${pollId}/results/`);
}

async function castVote(pollId, positionId, candidateId) {
    const data = {
        position: positionId,
        candidate: candidateId
    };
    
    return await apiRequest(`/polls/${pollId}/vote/`, 'POST', data);
}

// UI Functions
function updateNavbar() {
    const navbarContainer = document.getElementById('navbar-container');
    if (!navbarContainer) return;
    
    if (currentUser) {
        navbarContainer.innerHTML = `
            <ul class="nav-links">
                <li><a href="index.html">Home</a></li>
                <li><a href="polls.html">Polls</a></li>
                <li><a href="#" id="logout-btn">Logout (${currentUser.username})</a></li>
            </ul>
        `;
        
        document.getElementById('logout-btn').addEventListener('click', (e) => {
            e.preventDefault();
            logoutUser();
        });
    } else {
        navbarContainer.innerHTML = `
            <ul class="nav-links">
                <li><a href="index.html">Home</a></li>
                <li><a href="login.html">Login</a></li>
                <li><a href="register.html">Register</a></li>
            </ul>
        `;
    }
}

// Initialize
function initApp() {
    updateNavbar();
    
    // Check if user is authenticated
    if (!authToken && window.location.pathname !== '/login.html' && window.location.pathname !== '/register.html' && window.location.pathname !== '/index.html') {
        window.location.href = '/login.html';
    }
    
    // Initialize page-specific functionality
    const currentPage = window.location.pathname.split('/').pop();
    
    switch(currentPage) {
        case 'register.html':
            initRegisterPage();
            break;
        case 'login.html':
            initLoginPage();
            break;
        case 'polls.html':
            initPollsPage();
            break;
        case 'poll-detail.html':
            initPollDetailPage();
            break;
        case 'poll-results.html':
            initPollResultsPage();
            break;
    }
}

// Page-specific initializations
function initRegisterPage() {
    const registerForm = document.getElementById('register-form');
    if (!registerForm) return;
    
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Clear any existing alerts
        const alertContainer = document.getElementById('alert-container');
        if (alertContainer) {
            alertContainer.innerHTML = '';
        }
        
        const userData = {
            username: document.getElementById('username').value.trim(),
            password: document.getElementById('password').value,
            password2: document.getElementById('password2').value,
            email: document.getElementById('email').value.trim(),
            first_name: document.getElementById('first_name').value.trim(),
            last_name: document.getElementById('last_name').value.trim(),
            phone_number: document.getElementById('phone_number').value.trim()
        };
        
        // Basic validation
        if (!userData.username || !userData.password || !userData.email || !userData.first_name || !userData.last_name) {
            showAlert('Please fill in all required fields');
            return;
        }
        
        if (userData.password !== userData.password2) {
            showAlert('Passwords do not match');
            return;
        }
        
        if (userData.password.length < 8) {
            showAlert('Password must be at least 8 characters long');
            return;
        }
        
        // Disable submit button to prevent double submission
        const submitBtn = registerForm.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        submitBtn.disabled = true;
        submitBtn.textContent = 'Registering...';
        
        try {
            const success = await registerUser(userData);
            if (success) {
                showAlert('Registration successful! Redirecting...', 'success');
                setTimeout(() => {
                    window.location.href = '/polls.html';
                }, 1000);
            }
        } catch (error) {
            console.error('Registration error:', error);
        } finally {
            // Re-enable submit button
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;
        }
    });
}

function initLoginPage() {
    const loginForm = document.getElementById('login-form');
    if (!loginForm) return;
    
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const credentials = {
            username: document.getElementById('username').value,
            password: document.getElementById('password').value
        };
        
        const success = await loginUser(credentials);
        if (success) {
            window.location.href = '/polls.html';
        }
    });
}

async function initPollsPage() {
    const pollsContainer = document.getElementById('polls-container');
    if (!pollsContainer) return;
    
    const polls = await getPolls();
    if (!polls) return;
    
    if (polls.length === 0) {
        pollsContainer.innerHTML = '<p>No polls available at the moment.</p>';
        return;
    }
    
    let pollsHTML = '<div class="grid">';
    
    polls.forEach(poll => {
        pollsHTML += `
            <div class="card">
                <h2 class="card-title">${poll.title}</h2>
                <div class="card-body">
                    <p>${poll.description || 'No description available.'}</p>
                    <p class="mb-2">Start Time: ${formatDate(poll.start_time)}</p>
                    <p>Duration: ${poll.duration} hours</p>
                </div>
                <div class="card-footer">
                    <span class="poll-status ${getStatusClass(poll.status)}">${poll.status}</span>
                    <a href="poll-detail.html?id=${poll.id}" class="btn">View Details</a>
                </div>
            </div>
        `;
    });
    
    pollsHTML += '</div>';
    pollsContainer.innerHTML = pollsHTML;
}

async function initPollDetailPage() {
    const pollDetailContainer = document.getElementById('poll-detail-container');
    if (!pollDetailContainer) return;
    
    const urlParams = new URLSearchParams(window.location.search);
    const pollId = urlParams.get('id');
    
    if (!pollId) {
        window.location.href = '/polls.html';
        return;
    }
    
    const poll = await getPollDetails(pollId);
    if (!poll) return;
    
    let detailHTML = `
        <h1>${poll.title}</h1>
        <p class="mb-2">${poll.description || 'No description available.'}</p>
        <div class="mb-3">
            <p>Start Time: ${formatDate(poll.start_time)}</p>
            <p>End Time: ${formatDate(poll.end_time)}</p>
            <p class="mb-1">Status: <span class="poll-status ${getStatusClass(poll.status)}">${poll.status}</span></p>
        </div>
    `;
    
    if (poll.status === 'Ended') {
        detailHTML += `
            <div class="mb-3">
                <a href="poll-results.html?id=${poll.id}" class="btn">View Results</a>
            </div>
        `;
    }
    
    if (poll.positions.length === 0) {
        detailHTML += '<p>No positions available for this poll.</p>';
    } else {
        poll.positions.forEach(position => {
            detailHTML += `
                <h2 class="position-title">${position.title}</h2>
                <p class="mb-2">${position.description || 'No description available.'}</p>
            `;
            
            if (position.candidates.length === 0) {
                detailHTML += '<p>No candidates available for this position.</p>';
            } else {
                position.candidates.forEach(candidate => {
                    const imgSrc = candidate.profile_picture || 'static/images/default-profile.png';
                    
                    detailHTML += `
                        <div class="candidate">
                            <img src="${imgSrc}" alt="${candidate.name}" class="candidate-image">
                            <div class="candidate-info">
                                <h3 class="candidate-name">${candidate.name}</h3>
                                <p class="candidate-description">${candidate.description}</p>
                            </div>
                            ${poll.status === 'Active' ? 
                                `<button class="btn vote-btn" data-position="${position.id}" data-candidate="${candidate.id}">Vote</button>` : 
                                ''
                            }
                        </div>
                    `;
                });
            }
        });
    }
    
    pollDetailContainer.innerHTML = detailHTML;
    
    // Add event listeners to vote buttons
    if (poll.status === 'Active') {
        const voteButtons = document.querySelectorAll('.vote-btn');
        voteButtons.forEach(button => {
            button.addEventListener('click', async () => {
                const positionId = button.dataset.position;
                const candidateId = button.dataset.candidate;
                
                const result = await castVote(pollId, positionId, candidateId);
                if (result) {
                    showAlert('Vote cast successfully!', 'success');
                    // Disable all vote buttons for this position
                    document.querySelectorAll(`.vote-btn[data-position="${positionId}"]`).forEach(btn => {
                        btn.disabled = true;
                        btn.textContent = 'Voted';
                        btn.classList.add('btn-secondary');
                    });
                }
            });
        });
    }
}

async function initPollResultsPage() {
    const resultsContainer = document.getElementById('results-container');
    if (!resultsContainer) return;
    
    const urlParams = new URLSearchParams(window.location.search);
    const pollId = urlParams.get('id');
    
    if (!pollId) {
        window.location.href = '/polls.html';
        return;
    }
    
    const results = await getPollResults(pollId);
    if (!results) return;
    
    let resultsHTML = `
        <h1>${results.title} Results</h1>
        <p class="mb-3">Status: <span class="poll-status ${getStatusClass(results.status)}">${results.status}</span></p>
    `;
    
    if (results.positions.length === 0) {
        resultsHTML += '<p>No positions available for this poll.</p>';
    } else {
        results.positions.forEach(position => {
            resultsHTML += `
                <div class="result-position">
                    <h2 class="result-title">${position.title}</h2>
            `;
            
            if (position.winner) {
                resultsHTML += `
                    <div class="result-winner">
                        <span class="winner-label">Winner</span>
                        <strong>${position.winner.name}</strong> with ${position.winner.vote_count} votes
                    </div>
                `;
            } else if (results.status === 'Ended') {
                resultsHTML += `<p class="mb-2">No votes were cast for this position.</p>`;
            } else {
                resultsHTML += `<p class="mb-2">Results will be available when the poll ends.</p>`;
            }
            
            if (position.candidates && position.candidates.length > 0) {
                resultsHTML += `<ul class="result-candidates">`;
                position.candidates.forEach(candidate => {
                    resultsHTML += `
                        <li class="result-candidate">
                            <span>${candidate.name}</span>
                            <span class="vote-count">${candidate.vote_count} votes</span>
                        </li>
                    `;
                });
                resultsHTML += `</ul>`;
            }
            
            resultsHTML += `</div>`;
        });
    }
    
    resultsContainer.innerHTML = resultsHTML;
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', initApp);