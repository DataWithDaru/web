"""Generate the portfolio pages (warm-grey retro theme). Run from the repo root: python3 _build/gen.py .
(GitHub Pages ignores folders starting with "_", so this file is not published.)"""
import hashlib, os, sys
os.chdir(sys.argv[1])

def asset(path):
    # Version from the file's content, so browsers refetch it whenever it changes.
    return f"{path}?v={hashlib.sha256(open(path, 'rb').read()).hexdigest()[:10]}"

BASE = 'https://datawithdaru.github.io/web/'
CV = 'files/Daru Broodryk CV.docx'
LINKEDIN = 'https://www.linkedin.com/in/daru-broodryk-609192139/'
GITHUB = 'https://github.com/DataWithDaru'

NAV = [('index.html', 'Home'), ('databases.html', 'Data Engineering'), ('data_science.html', 'AI'), ('people.html', 'People'), ('index.html#contact', 'Contact')]

def head(title, desc, path):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8" />
	<meta name="viewport" content="width=device-width, initial-scale=1" />
	<title>{title}</title>
	<meta name="description" content="{desc}" />
	<meta property="og:title" content="{title}" />
	<meta property="og:description" content="{desc}" />
	<meta property="og:type" content="website" />
	<meta property="og:url" content="{BASE}{'' if path == 'index.html' else path}" />
	<meta property="og:image" content="{BASE}images/portrait.webp" />
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
	<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&amp;family=Inter:wght@400;500;600&amp;display=swap" />
	<link rel="stylesheet" href="{asset('assets/css/site.css')}" />
	<script>document.documentElement.classList.add('js');</script>
</head>
<body>
	<a class="skip-link" href="#main">Skip to content</a>
'''

def header(current):
    items = ''.join(
        f'\t\t\t\t<li><a href="{h}"{" aria-current=\"page\"" if h == current else ""}>{t}</a></li>\n' for h, t in NAV)
    return f'''	<header class="site-header">
		<a class="logo" href="index.html" aria-label="Daru Broodryk portfolio, home">PORTFOLIO</a>
		<button class="menu-toggle" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
		<nav class="nav" id="nav" aria-label="Main">
			<ul>
{items}			</ul>
			<a class="header-cta" href="{CV}" download>CV</a>
		</nav>
	</header>
'''

CONTACT = f'''		<section class="section contact" id="contact">
			<div class="wrap">
				<p class="eyebrow reveal">Contact</p>
				<h2 class="display reveal">Let’s build something great together</h2>
				<div class="contact-grid">
					<form class="form reveal" method="POST" action="https://formsubmit.co/dbroodryk@outlook.com">
						<div class="field"><label for="name">Name</label><input type="text" id="name" name="name" autocomplete="name" required /></div>
						<div class="field"><label for="email">Email</label><input type="email" id="email" name="email" autocomplete="email" required /></div>
						<div class="field full"><label for="message">Message</label><textarea id="message" name="message" rows="3"></textarea></div>
						<input type="hidden" name="_next" value="{BASE}thankyou.html" />
						<input type="hidden" name="_subject" value="New message from datawithdaru.github.io" />
						<button class="btn btn-solid" type="submit">Send <span class="arrow" aria-hidden="true">→</span></button>
					</form>
					<div class="link-cols reveal">
						<div>
							<h3>Pages</h3>
							<ul>
								<li><a href="index.html">Home</a></li>
								<li><a href="databases.html">Data Engineering</a></li>
								<li><a href="data_science.html">Artificial Intelligence</a></li>
								<li><a href="people.html">People</a></li>
							</ul>
						</div>
						<div>
							<h3>Elsewhere</h3>
							<ul>
								<li><a href="{LINKEDIN}">LinkedIn</a></li>
								<li><a href="{GITHUB}">GitHub</a></li>
								<li><a href="{CV}" download>Download CV</a></li>
							</ul>
						</div>
					</div>
				</div>
			</div>
		</section>
'''

def footer(contact=True):
    return (CONTACT if contact else '') + '''	</main>
	<footer class="wrap site-footer">
		<span>© 2026 Daru Broodryk</span>
		<a href="#top">Back to top ↑</a>
	</footer>
	<script src="''' + asset('assets/js/site.js') + '''"></script>
</body>
</html>
'''

LOGOS = {  # single-colour masks; --lh is the optical height in px
    'aa': ('images/logos/aa.svg', '1', 40, 'AA'),
    'onenz': ('images/logos/onenz.svg', '558.2 / 102', 20, 'One NZ'),
    'mitre10': ('images/logos/mitre10.svg', '175 / 56', 34, 'Mitre 10'),
    'firn': ('images/logos/firn.png', '640 / 209', 26, 'FIRN Analytics'),
}

def logo(key, scale=1.0):
    src, ar, lh, name = LOGOS[key]
    # url() set inline so it resolves against the page, not the stylesheet
    return f'<span class="logo-mark" role="img" aria-label="{name} logo" style="-webkit-mask-image: url({src}); mask-image: url({src}); --ar: {ar}; --lh: {round(lh * scale)}px;"></span>'

def esc_tags(tags):
    return ''.join(f'<span class="tag">{t}</span>' for t in tags)

# ---------------------------------------------------------------- content
WORK = [
    dict(logo='onenz', href='databases.html#onenz', date='Current', pitch='Moving a data platform with confidence.',
         tags=['Data Engineering', 'Migration', 'Automation'], stat='Now', caption='dbt platform migration', a='#817e60', b='#33322a'),
    dict(logo='mitre10', href='databases.html#mitre10', date='3 months', pitch='A clear picture of platform health.',
         tags=['Snowflake', 'Platform review'], stat='3', label='month engagement', a='#9c7462', b='#3b2a23'),
    dict(logo='aa', href='databases.html#aa', date='12 months', pitch='One trusted data platform.',
         tags=['Data Engineering', 'dbt', 'Snowflake'], stat='12', label='month engagement', a='#738084', b='#2c3639'),
    dict(logo='firn', href='data_science.html#knowledge-base', date='2 months', pitch='Helping a whole firm use AI safely.',
         tags=['Artificial Intelligence', 'Claude Code', 'Python'], stat='2', label='month engagement', a='#5f616b', b='#212228'),
]

AREAS = [
    ('databases.html', 'Data Engineering', 'Snowflake, dbt Cloud, dbt Core and platform migrations'),
    ('data_science.html', 'Artificial Intelligence', 'Claude Code, AI enablement and machine learning'),
    ('people.html', 'People', 'Leadership, mentoring and AI adoption'),
]

def areas_list():
    return '\t\t\t\t<ul class="areas">\n' + ''.join(
        f'\t\t\t\t\t<li class="reveal"><a href="{h}"><span class="num">0{i}</span><span class="display">{t}</span><span class="desc">{d}</span></a></li>\n'
        for i, (h, t, d) in enumerate(AREAS, 1)) + '\t\t\t\t</ul>\n'

TESTIMONIAL_ITEMS = [
    ('Data Modelling', 'A key Data Engineer across all releases, supporting development, testing and production deployment.'),
    ('Data Protection &amp; Classification', 'Led the implementation of our data protection and classification capability, including governance artefacts.'),
    ('Platform Migration', 'Supported a pilot migration, helping ensure successful reconciliation and deployment outcomes.'),
    ('Data Engineering &amp; Platform Development', 'Built data models, reusable engineering patterns and governance controls that continue to underpin the platform.'),
    ('Data Governance &amp; Quality', 'Contributed to data classification standards, data quality improvements and the ongoing evolution of our data governance practices.'),
    ('Knowledge Transfer &amp; Innovation', 'Consistently shared knowledge through documentation, handovers and workshops, while introducing new ideas in areas such as automation, synthetic data and platform governance.'),
]

# ---------------------------------------------------------------- index
def index():
    cards = ''
    for w in WORK:
        cards += f'''				<a class="work-card reveal" href="{w['href']}" style="--card-a: {w['a']}; --card-b: {w['b']};">
					<span class="art" aria-hidden="true"></span>
					<p class="stat" aria-hidden="true">{w['stat']}</p>
					<span class="inner">
						<span class="brand">{logo(w['logo']) if w.get('logo') else ''}</span>
{f'''						<span class="display title">{w['title']}</span>
''' if w.get('title') else ''}						<span class="display date">{w['date']}</span>
						<span class="display pitch">{w['pitch']}</span>
						<span class="tags">{esc_tags(w['tags'])}</span>
					</span>
					<p class="stat-label">{w.get('caption') or w['stat'] + ' ' + w['label']}</p>
				</a>
'''
    letter_items = ''.join(f'\t\t\t\t\t\t\t<li><strong>{t}</strong>{d}</li>\n' for t, d in TESTIMONIAL_ITEMS)
    body = f'''{head('Daru Broodryk | Senior Consultant', 'Daru Broodryk, Senior Consultant at FIRN Analytics in Auckland: Snowflake and dbt platforms, AI enablement with Claude Code, and the people side of data.', 'index.html')}{header('index.html')}	<main id="main">
		<section class="hero" id="top" aria-label="Introduction">
			<div class="code-word" data-word="Daru" aria-hidden="true"><canvas></canvas></div>
			<img class="hero-portrait" src="images/portrait.webp" width="585" height="774" alt="Daru Broodryk" fetchpriority="high" />
			<div class="hero-meta">
				<div>
					<h1 class="role">Daru Broodryk<br />Senior Consultant</h1>
					<p>FIRN Analytics · Auckland</p>
				</div>
				<p class="scroll-cue">Scroll</p>
			</div>
		</section>

		<section class="section" id="story">
			<div class="wrap intro">
				<div>
					<p class="eyebrow reveal">My story</p>
					<h2 class="display statement" data-fill="trust and act on it">Data is only useful when people trust and act on it. That’s where I come in.</h2>
				</div>
				<div class="intro-copy reveal">
					<p>I’m a <strong>Senior Consultant at FIRN Analytics</strong> in Auckland. I have been building solutions and enabling teams to work smarter for over 10 years.</p>
					<div class="actions">
						<a class="btn btn-solid" href="{CV}" download>Download CV</a>
						<a class="btn" href="#work">My work <span class="arrow" aria-hidden="true">›</span></a>
					</div>
				</div>
			</div>
		</section>

		<section class="section" id="areas">
			<div class="wrap">
				<p class="eyebrow reveal">Explore by area</p>
{areas_list()}			</div>
		</section>

		<section class="section" id="work">
			<div class="wrap">
				<div class="section-head">
					<h2 class="display reveal">Projects</h2>
				</div>
				<div class="work-list">
{cards}				</div>
			</div>
		</section>

		<section class="section testimonial" id="kind-words">
			<div class="wrap">
				<p class="eyebrow reveal">Kind words</p>
				<h2 class="display quote" data-fill="lasting impact">“His work has left a lasting impact on our platform, governance capabilities and ways of working.”</h2>
				<div class="testimonial-body">
					<div class="reveal">
						<p class="attribution"><strong>Data &amp; analytics leader</strong>Client engagement</p>
					</div>
					<div class="letter reveal">
						<p>With Daru’s contract coming to an end this week, I’d like to acknowledge his contribution over the past year and thank him for the expertise, commitment, and support he’s brought to the team. Daru Broodryk joined us through FIRN and has made a significant contribution to the growth and maturity of our data platform. Some of his key contributions include:</p>
						<ul>
{letter_items}						</ul>
						<p>Throughout his time with us, Daru combined strong technical capability with a practical, collaborative approach. His work has left a lasting impact on our platform, governance capabilities and ways of working. I have personally really enjoyed working with Daru and wish him every success in his next chapter.</p>
					</div>
				</div>
			</div>
		</section>

{footer()}'''
    return body

# ---------------------------------------------------------------- inner pages
def entry(n, eid, title, meta, paras, tags=(), link=None, href=None, extra='', brand=None):
    t = f'<a href="{href}">{title}</a>' if href else title
    ps = ''.join(f'\t\t\t\t\t\t<p>{p}</p>\n' for p in paras)
    tg = f'\t\t\t\t\t\t<div class="tags">{esc_tags(tags)}</div>\n' if tags else ''
    lk = f'\t\t\t\t\t\t<a class="link" href="{link[0]}">{link[1]} →</a>\n' if link else ''
    m = ''.join(f'{x}<br />' for x in meta[:-1]) + meta[-1]
    return f'''				<article class="entry reveal" id="{eid}">
					<div class="entry-meta">{logo(brand) if brand else ''}<div class="num">{n:02d}</div><p>{m}</p></div>
					<div class="body">
						<h3 class="display">{t}</h3>
{ps}{tg}{lk}{extra}					</div>
				</article>
'''

def chapter(cid, title, entries):
    return f'''		<section class="chapter" id="{cid}">
			<div class="wrap">
				<h2 class="display chapter-title reveal">{title}</h2>
{''.join(entries)}			</div>
		</section>
'''

def page(path, title, desc, ghost, h1, lede, chapters, nxt):
    nh, nt = nxt
    return f'''{head(title, desc, path)}{header(path)}	<main id="main">
		<section class="page-hero" id="top">
			<div class="code-word" data-word="{ghost}" aria-hidden="true"><canvas></canvas></div>
			<div class="wrap">
				<p class="eyebrow">Projects</p>
				<h1 class="display">{h1}</h1>
				<p class="lede">{lede}</p>
			</div>
		</section>
{''.join(chapters)}		<div class="wrap"><a class="next-page" href="{nh}"><span class="eyebrow">Next</span><span class="display">{nt} →</span></a></div>
{footer()}'''

FIRN = 'FIRN Analytics'
de = page('databases.html', 'Daru Broodryk | Data Engineering',
    'Data engineering by Daru Broodryk: Snowflake and dbt platforms for the AA, One NZ and Mitre 10.',
    'Data', 'Data Engineering',
    'Understanding data and shaping it is my bread and butter. These days that means modern Snowflake and dbt platforms for some of New Zealand’s best-known organisations.',
    [chapter('recent-work', 'Recent work', [
        entry(1, 'aa', 'NZ Automobile Association – Data Platform', ['Senior Data Engineer', FIRN, '12 months'],
              ['I was a senior data engineer on the AA’s enterprise data platform on Snowflake, dbt Cloud and dbt Core, working across the layers from source through to reporting.',
               'I led the data protection and classification capability, and contributed to data modelling, data quality, governance and platform modernisation.'],
              ['dbt Cloud', 'dbt Core', 'Snowflake', 'Data modelling', 'Data governance'], brand='aa'),
        entry(2, 'onenz', 'One NZ – Data Platform Migration', ['AI Solution Architect', FIRN, 'Current'],
              ['I’m delivering a data platform migration for One NZ, from planning and discovery through to automation and cutover.',
               'I wrote the migration plan, built read-only discovery tooling, and designed the automation and testing approach for moving workloads safely.'],
              ['dbt Cloud', 'dbt Projects', 'Snowflake', 'Migration', 'Automation', 'Claude Code'], brand='onenz'),
        entry(3, 'mitre10', 'Mitre 10 – Snowflake Platform Review', ['Senior Data Engineer', FIRN, '3 months'],
              ['I reviewed Mitre 10’s Snowflake platform end to end, using read-only evidence and stakeholder input to give a clear picture of the platform’s health.'],
              ['Snowflake', 'SQL', 'Platform review'], brand='mitre10'),
        entry(4, 'toolkit', 'Toolkit across engagements', ['All clients'],
              ['Across my client work I use modern data engineering tools and practices, from orchestration and CI/CD through to automated testing and code quality.'],
              ['dbt Cloud', 'dbt Core', 'Snowflake', 'SQL/Jinja', 'Python', 'PowerShell', 'Apache Airflow', 'CI/CD pipelines', 'Data testing']),
     ])],
    ('data_science.html', 'Artificial Intelligence'))

ai = page('data_science.html', 'Daru Broodryk | Artificial Intelligence',
    'AI work by Daru Broodryk: AI enablement with Claude Code and machine learning projects.',
    'Intelligence', 'Super Intelligence',
    'I help teams put AI to work safely: giving it the firm’s own knowledge, sensible guardrails, and tools people actually use.',
    [chapter('ai-enablement', 'AI enablement', [
        entry(1, 'knowledge-base', 'FIRN AI Enablement', ['AI Solution Architect', FIRN, '2 months'],
              ['A shared knowledge base that lets Claude Code draw on the firm’s own practice and process knowledge, and an internal plugin marketplace that distributes version-controlled, reviewed AI skills across the firm.',
               'I built the knowledge base structure, the import pipelines, a RAG search layer, rule enforcement, and the installer and update flow. I also built the core plugin and its skills, added guardrails that block personal data, and vetted the third-party plugins we adopt.'],
              ['Claude Code (plugins, skills, hooks)', 'RAG', 'Python', 'PowerShell', 'Node.js', 'Git/GitHub', 'pytest'], brand='firn'),
     ]),
     chapter('machine-learning', 'Machine learning', [
        entry(2, 'ml-fundamentals', 'Machine Learning Fundamentals', ['Notebook'],
              ['My first steps into machine learning: loading data into a model and training it to make predictions.'],
              ['Python', 'TensorFlow', 'pandas'], href='FirstAI.html', link=('FirstAI.html', 'Open the notebook')),
        entry(3, 'image-classification', 'Image Classification', ['Notebook'],
              ['Going further into machine learning, this time teaching a model to classify images.'],
              ['Python', 'TensorFlow', 'NumPy', 'matplotlib'], href='ClasifyImages.html', link=('ClasifyImages.html', 'Open the notebook')),
     ])],
    ('people.html', 'People'))

ppl = page('people.html', 'Daru Broodryk | People',
    'Leadership, mentoring, knowledge sharing and AI adoption: how Daru Broodryk works with people.',
    'People', 'People',
    'Data work is people work. Here’s how I lead, teach and work with the people around me.',
    [chapter('how-i-work', 'How I work with people', [
        entry(1, 'mentor', 'Mentoring, hiring and training', ['Technical Support', 'Concourse IT', '2019 – 2021'],
              ['I managed a small team of junior support agents and was their escalation point for advanced issues. I reviewed and approved their SQL scripts before they reached the Business Intelligence team, helped interview new hires by testing their database skills, and trained new starters on both the application and SQL.']),
        entry(2, 'lead', 'Leading a data team', ['Data Services Account Lead', 'Altis Consulting', '2024 – 2025'],
              ['I led a small team of data engineers looking after client data platforms across healthcare, insurance, energy, education and retail. I set clear rules of engagement and handover strategies, resolved technical escalations, kept pipelines and data warehouses running to schedule, and worked on pre-sales, estimation and invoicing for new projects.']),
        entry(3, 'knowledge', 'Sharing knowledge', ['NZ Automobile Association', FIRN],
              ['On every engagement I leave knowledge behind, not just code, sharing what I know through documentation, handovers and workshops.']),
        entry(4, 'adoption', 'Driving AI adoption', ['AI Solution Architect', FIRN],
              ['Good AI tooling only matters if people use it. At FIRN I build the shared knowledge base and plugin marketplace my colleagues use every day, vet the third-party tools we adopt, and build in guardrails such as personal-data blocking so the whole team can use AI with confidence.']),
        entry(5, 'stakeholders', 'Working with stakeholders', ['Every role since 2019'],
              ['From analysts and finance managers to CEOs and CTOs, I work directly with the people who rely on the data: understanding what they need, explaining the trade-offs in plain language, and building trust that what we deliver is right.']),
     ])],
    ('databases.html', 'Data Engineering'))

projects = f'''{head('Daru Broodryk | Projects', 'Projects by Daru Broodryk across data engineering, artificial intelligence and people leadership.', 'projects.html')}{header('')}	<main id="main">
		<section class="page-hero" id="top">
			<div class="code-word" data-word="Work" aria-hidden="true"><canvas></canvas></div>
			<div class="wrap">
				<p class="eyebrow">Projects</p>
				<h1 class="display">Projects</h1>
				<p class="lede">My work, grouped into three areas.</p>
			</div>
		</section>
		<section class="chapter">
			<div class="wrap">
{areas_list()}			</div>
		</section>
{footer()}'''

def simple(path, title, ghost, h1, lede, contact):
    return f'''{head(title, lede, path)}{header('')}	<main id="main">
		<section class="page-hero" id="top" style="min-height: 70vh;">
			<div class="code-word" data-word="{ghost}" aria-hidden="true"><canvas></canvas></div>
			<div class="wrap">
				<h1 class="display">{h1}</h1>
				<p class="lede">{lede}</p>
				<div class="actions" style="margin-top: 32px;"><a class="btn btn-solid" href="index.html">Back home</a><a class="btn" href="index.html#work">See my work <span class="arrow" aria-hidden="true">›</span></a></div>
			</div>
		</section>
{footer(contact)}'''

pages = {
    'index.html': index(),
    'databases.html': de,
    'data_science.html': ai,
    'people.html': ppl,
    'projects.html': projects,
    '404.html': simple('404.html', 'Daru Broodryk | Page not found', '404', 'Page not found', 'That page doesn’t exist, or it has moved.', False),
    'thankyou.html': simple('thankyou.html', 'Daru Broodryk | Thank you', 'Thanks', 'Message sent', 'Thanks for getting in touch. I’ll get back to you soon.', False),
}
for f, html in pages.items():
    open(f, 'w', newline='\n').write(html)
    print('wrote', f, len(html))
