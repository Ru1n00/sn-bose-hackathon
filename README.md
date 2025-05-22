# 🎓 Edutech – An Educational Social Platform with Gamification & Accessibility

**Edutech** is a Django-powered progressive web platform designed to make learning interactive, accessible, and community-driven. It enables users to post and discover educational content, take quizzes, track learning progress with streaks and leaderboards, translate content to Bangla, and participate in citizen-driven surveys and data collection — all with a modern, responsive interface built using Tailwind CSS and Alpine.js.

---

## 🚀 Features

### 📝 Content Sharing & Engagement
- Post and explore educational content (videos, PDFs, images, text)
- Upvote/downvote and comment on posts
- Threaded replies for interactive discussions

### 🧠 Gamified Quizzes
- Take quizzes by topic/subject
- Score-based feedback and progress tracking
- Maintain daily streaks to stay consistent
- Leaderboard to motivate friendly competition

### 🌍 Accessibility & Inclusion
- English-to-Bangla translation via Google Translate API
- Support for lower literacy levels through audio-visual aids
- Mobile-first design for rural accessibility

### 📊 Surveys & Citizen Science
- Create and participate in surveys
- Collect structured data for educational or scientific use
- Visualize submissions and contributions

### 🔥 Offline-Friendly (PWA-ready)
- Designed with future support for offline access via service workers
- Fast and responsive user experience across devices

---

## 🛠️ Tech Stack

### Backend
- [Django](https://www.djangoproject.com/) – Core web framework
- SQLite (default) / PostgreSQL (optional)

### Frontend
- HTML + [Tailwind CSS](https://tailwindcss.com/)
- [Alpine.js](https://alpinejs.dev/) + Vanilla JavaScript

### UI Drsign
- [Figma UI](https://www.figma.com/design/WegwCD41waTsEjXzrL0vwL/404-Not-Founder?node-id=0-1&t=fc1na33N3DkZMesb-1) – View the figma file from here
  
### Tools & Packages
- `python -m venv venv` – Python virtual environment
- `requirements.txt` – Python package dependencies
- `runtime.txt` – For deployment compatibility
- `django-google-translate` – Content translation
- `pytranscript` – Video/audio subtitle generation

---

## 🧪 Getting Started

### 🔧 1. Clone the Repository
```bash
git clone https://github.com/Ru1n00/sn-bose-hackathon/
cd edutech
```

### 📦 2. Set Up Virtual Environment
```bash
cd main_app/
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 📥 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### ⚙️ 4. Configure Environment Variables
Create a `.env` file in the root directory and add your environment variables:
```env
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,
```

### 🗄️ 5. Database Setup
```bash
python manage.py migrate
```

### 📂 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 🚀 7. Run the Development Server
```bash
python manage.py runserver
```

## 🧠 Key Modules & Highlights

| Feature                      | Description                                                                          |
|-----------------------------|--------------------------------------------------------------------------------------|
| 🔗 Educational Content Feed  | Users can create, browse, and interact with posts containing educational materials   |
| 🧠 Quiz System               | Topic-based quizzes with score tracking and instant feedback                         |
| 🔥 Gamification              | Daily streaks, point system, and subject-wise leaderboards                           |
| 🌍 Bangla Translation        | Auto-translate content from English to Bangla using Google Translate API            |
| 📊 Survey System             | Create and submit structured surveys; collect and display citizen-contributed data   |
| 🧪 Citizen Science           | Participate in real-world science projects through data collection tools             |
| 💬 Community Interaction     | Upvotes, downvotes, comments, threaded replies, and contributor recognition          |
| 📱 PWA-ready                 | Future support for offline access and service workers                               


## 📜 License

This project is licensed under the **MIT License**.

You are free to use, modify, and distribute this project for personal or commercial use, provided that the original license is included with any substantial portions of the software.

See the [LICENSE](LICENSE) file for more details.
