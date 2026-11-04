/* Daru Broodryk portfolio: hero intro, scroll reveals, word hover fills, parallax, mobile menu */
(function () {
	var root = document.documentElement;
	var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

	// Hero intro plays once fonts and the portrait are ready (with a safety timeout).
	function loaded() { root.classList.add('is-loaded'); }
	var portrait = document.querySelector('.hero-portrait');
	if (portrait && !portrait.complete) {
		portrait.addEventListener('load', loaded);
		portrait.addEventListener('error', loaded);
		setTimeout(loaded, 2500);
	} else {
		requestAnimationFrame(loaded);
	}

	// Mobile menu.
	var toggle = document.querySelector('.menu-toggle');
	var nav = document.getElementById('nav');
	if (toggle && nav) {
		toggle.addEventListener('click', function () {
			var open = nav.classList.toggle('is-open');
			toggle.setAttribute('aria-expanded', open);
			toggle.textContent = open ? 'Close' : 'Menu';
		});
		nav.addEventListener('click', function (e) {
			if (e.target.closest('a')) {
				nav.classList.remove('is-open');
				toggle.setAttribute('aria-expanded', 'false');
				toggle.textContent = 'Menu';
			}
		});
	}

	// Split statements into words so they can fill in as you scroll.
	var fills = Array.prototype.slice.call(document.querySelectorAll('[data-fill]'));
	fills.forEach(function (el) {
		var words = el.textContent.trim().split(/\s+/);
		el.setAttribute('aria-label', el.textContent.trim());
		// data-fill="trust act" lights only those words; a bare data-fill lights every word.
		var only = (el.getAttribute('data-fill') || '').toLowerCase().split(/\s+/).filter(Boolean);
		el.innerHTML = words.map(function (w, i) {
			var lit = !only.length || only.indexOf(w.toLowerCase().replace(/[^a-z]/g, '')) > -1;
			return '<span class="w' + (lit ? ' lit' : '') + '" aria-hidden="true" style="--i: ' + i + '">' + w.replace(/&/g, '&amp;').replace(/</g, '&lt;') + '</span>';
		}).join(' ');
	});

	// Reveal blocks as they enter the viewport.
	var reveals = document.querySelectorAll('.reveal');
	if ('IntersectionObserver' in window && !reduce) {
		var io = new IntersectionObserver(function (entries) {
			entries.forEach(function (en) {
				if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
			});
		}, { rootMargin: '0px 0px -10% 0px' });
		reveals.forEach(function (el) { io.observe(el); });
	} else {
		reveals.forEach(function (el) { el.classList.add('is-in'); });
	}

	var header = document.querySelector('.site-header');
	var ghosts = Array.prototype.slice.call(document.querySelectorAll('.ghost-word'));
	var lastY = window.scrollY;
	var ticking = false;

	function update() {
		ticking = false;
		var y = window.scrollY;
		var vh = window.innerHeight;

		if (header) {
			header.classList.toggle('is-scrolled', y > 10);
			var navOpen = nav && nav.classList.contains('is-open');
			header.classList.toggle('is-hidden', !navOpen && y > lastY && y > vh * 0.6);
		}
		lastY = y;

		if (reduce) return;
		ghosts.forEach(function (g) {
			var r = g.parentElement.getBoundingClientRect();
			if (r.bottom < 0 || r.top > vh) return;
			var p = (r.top + r.height / 2 - vh / 2) / vh;
			g.style.setProperty('--px', (p * 18) + 'vw');
		});
	}

	// "Disrupted code" background words: a grid of flickering monospace glyphs that
	// forms the word, with sparse accent blocks and the odd row glitching sideways.
	var GLYPHS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789{}[]<>/=+-*#%$&;:_'.split('');
	var INK = '51, 50, 46', ACCENT = '162, 141, 128';

	function codeWord(el) {
		var canvas = el.querySelector('canvas');
		var ctx = canvas.getContext('2d');
		var word = el.getAttribute('data-word');
		var cell, cols, rows, cover, glyph, accent, faint, glitch = {}, timer = null, visible = false;

		function rnd(n) { return Math.floor(Math.random() * n); }

		function build() {
			var w = el.clientWidth, h = el.clientHeight;
			if (!w || !h) return;
			var dpr = Math.min(window.devicePixelRatio || 1, 2);
			canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr);
			ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
			cell = w < 600 ? 10 : 13;
			cols = Math.ceil(w / cell); rows = Math.ceil(h / cell);

			// Rasterise the word at 4 samples per cell and keep each cell's coverage.
			var S = 4, off = document.createElement('canvas');
			off.width = cols * S; off.height = rows * S;
			var o = off.getContext('2d');
			var size = off.height * 0.9;
			o.font = '400 ' + size + 'px Anton, Impact, sans-serif';
			var m = o.measureText(word.toUpperCase());
			size *= Math.min(1, (off.width * 0.9) / m.width);
			o.font = '400 ' + size + 'px Anton, Impact, sans-serif';
			m = o.measureText(word.toUpperCase());
			var th = m.actualBoundingBoxAscent + m.actualBoundingBoxDescent;
			o.fillStyle = '#000';
			o.fillText(word.toUpperCase(), (off.width - m.width) / 2, (off.height - th) / 2 + m.actualBoundingBoxAscent);
			var data = o.getImageData(0, 0, off.width, off.height).data;

			var n = cols * rows;
			cover = new Float32Array(n); glyph = new Uint8Array(n); accent = new Uint8Array(n); faint = new Uint8Array(n);
			for (var r = 0; r < rows; r++) for (var c = 0; c < cols; c++) {
				var sum = 0;
				for (var y = 0; y < S; y++) for (var x = 0; x < S; x++) sum += data[(((r * S + y) * off.width) + c * S + x) * 4 + 3];
				var i = r * cols + c;
				cover[i] = sum / (S * S * 255);
				glyph[i] = rnd(GLYPHS.length);
				faint[i] = Math.random() < 0.035 ? 1 : 0;
				accent[i] = Math.random() < (cover[i] > 0.3 ? 0.01 : 0.002) ? 1 + rnd(2) : 0;
			}
			draw();
		}

		function draw() {
			var w = canvas.width, h = canvas.height;
			ctx.clearRect(0, 0, w, h);
			ctx.font = Math.round(cell * 0.92) + 'px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace';
			ctx.textBaseline = 'top';
			for (var r = 0; r < rows; r++) {
				var shift = glitch[r] || 0;
				for (var c = 0; c < cols; c++) {
					var src = c - shift;
					if (src < 0 || src >= cols) continue;
					var i = r * cols + src, k = cover[i], x = c * cell, y = r * cell;
					if (accent[i] === 1) {
						ctx.fillStyle = 'rgba(' + ACCENT + ', 0.8)';
						ctx.fillRect(x + cell * 0.18, y + cell * 0.08, cell * 0.6, cell * 0.84);
					} else if (accent[i] === 2) {
						ctx.fillStyle = 'rgba(' + ACCENT + ', 0.95)';
						ctx.fillText(GLYPHS[glyph[i]], x, y);
					} else if (k > 0.12) {
						ctx.fillStyle = 'rgba(' + INK + ', ' + (0.06 + 0.2 * k).toFixed(3) + ')';
						ctx.fillText(GLYPHS[glyph[i]], x, y);
					} else if (faint[i]) {
						ctx.fillStyle = 'rgba(' + INK + ', 0.09)';
						ctx.fillText(GLYPHS[glyph[i]], x, y);
					}
				}
			}
		}

		function tick() {
			if (!glyph) return; // fonts still loading, grid not built yet
			var n = cols * rows, changes = Math.ceil(n * 0.04);
			for (var j = 0; j < changes; j++) glyph[rnd(n)] = rnd(GLYPHS.length);
			for (var a = 0; a < 3; a++) { var p = rnd(n); if (accent[p]) { accent[p] = 0; accent[rnd(n)] = 1 + rnd(2); } }
			if (Math.random() < 0.08) {
				var row = rnd(rows), span = 1 + rnd(3), by = (Math.random() < 0.5 ? -1 : 1) * (1 + rnd(4));
				for (var s = 0; s < span; s++) glitch[row + s] = by;
				setTimeout(function () { for (var s2 = 0; s2 < span; s2++) delete glitch[row + s2]; }, 260);
			}
			draw();
		}

		function start() { if (!timer && !reduce) timer = setInterval(tick, 90); }
		function stop() { clearInterval(timer); timer = null; }

		var ready = document.fonts && document.fonts.load ? document.fonts.load('400 100px Anton') : Promise.resolve();
		ready.then(build, build);
		var resizeTimer;
		window.addEventListener('resize', function () { clearTimeout(resizeTimer); resizeTimer = setTimeout(build, 200); });
		if ('IntersectionObserver' in window) {
			new IntersectionObserver(function (en) {
				visible = en[0].isIntersecting;
				if (visible) start(); else stop();
			}).observe(el);
		} else {
			start();
		}
	}
	Array.prototype.forEach.call(document.querySelectorAll('.code-word'), codeWord);

	function onScroll() {
		if (!ticking) { ticking = true; requestAnimationFrame(update); }
	}
	window.addEventListener('scroll', onScroll, { passive: true });
	window.addEventListener('resize', onScroll);
	update();
})();
