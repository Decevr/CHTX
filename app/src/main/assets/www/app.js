(function () {
  var data = window.CATALOG;
  var view = "browse";
  var category = "all";
  var query = "";
  var main = document.getElementById("main");
  var menu = document.getElementById("category-menu");
  var menuToggle = document.getElementById("category-toggle");
  var menuPanel = document.getElementById("category-panel");
  var menuLabel = document.getElementById("category-label");
  var menuCount = document.getElementById("category-count");
  var menuOpen = false;
  var detail = document.getElementById("detail");
  var toast = document.getElementById("toast");
  var searchInput = document.getElementById("search");
  var clearButton = document.getElementById("clear-search");
  var status = document.getElementById("status");
  var finder = document.getElementById("finder");

  function byCategory(id) {
    if (id === "all") return data.characters;
    return data.characters.filter(function (row) { return row.category === id; });
  }

  function labelFor(id) {
    var found = data.categories.filter(function (row) { return row.id === id; })[0];
    return found ? found.label : id;
  }

  function matches(row, needle) {
    if (!needle) return true;
    return row.name.toLowerCase().indexOf(needle) !== -1 ||
      row.series.toLowerCase().indexOf(needle) !== -1;
  }

  function countFor(id) {
    var needle = query.trim().toLowerCase();
    var total = 0;
    data.characters.forEach(function (row) {
      if (id !== "all" && row.category !== id) return;
      if (matches(row, needle)) total += 1;
    });
    return total;
  }

  function openDetail(index) {
    var row = data.characters[index];
    detail.hidden = false;
    detail.scrollTop = 0;
    detail.innerHTML =
      '<div class="detail-bar"><button type="button" class="back" id="back">Back</button></div>' +
      '<img class="portrait" alt="">' +
      '<div class="detail-copy"><h2></h2><p class="meta"></p></div>' +
      '<article class="prompt"><h3>Character</h3><p id="positive"></p><button type="button" class="copy" id="copy-positive">Copy character</button></article>' +
      '<article class="prompt"><h3>Danbooru / Gelbooru</h3><p id="booru"></p><button type="button" class="copy" id="copy-booru">Copy tags</button></article>' +
      '<p class="note"></p>';
    detail.querySelector(".portrait").src = row.image;
    detail.querySelector("h2").textContent = row.name;
    detail.querySelector(".meta").textContent = row.series + " · " + labelFor(row.category);
    detail.querySelector("#positive").textContent = row.positive;
    detail.querySelector("#booru").textContent = row.booru || "";
    detail.querySelector(".note").textContent = data.settings.note;
    detail.querySelector("#back").addEventListener("click", closeDetail);
    detail.querySelector("#copy-positive").addEventListener("click", function () { copyText(row.positive); });
    detail.querySelector("#copy-booru").addEventListener("click", function () { copyText(row.booru || ""); });
  }

  function closeDetail() {
    detail.hidden = true;
    detail.innerHTML = "";
  }

  function copyText(text) {
    if (window.PromptAssist && window.PromptAssist.copy) {
      window.PromptAssist.copy(text);
    } else if (navigator.clipboard) {
      navigator.clipboard.writeText(text);
    }
    toast.hidden = false;
    clearTimeout(copyText.timer);
    copyText.timer = setTimeout(function () { toast.hidden = true; }, 1400);
  }

  function card(row) {
    var button = document.createElement("button");
    button.type = "button";
    button.className = "card";
    button.dataset.name = row.name.toLowerCase();
    button.dataset.series = row.series.toLowerCase();
    var image = document.createElement("img");
    image.alt = "";
    image.loading = "lazy";
    image.src = row.image;
    var copy = document.createElement("div");
    var title = document.createElement("h2");
    title.textContent = row.name;
    var series = document.createElement("p");
    series.textContent = row.series;
    copy.appendChild(title);
    copy.appendChild(series);
    button.appendChild(image);
    button.appendChild(copy);
    button.addEventListener("click", function () {
      openDetail(data.characters.indexOf(row));
    });
    return button;
  }

  function categoryItems() {
    return [{ id: "all", label: "All" }].concat(data.categories);
  }

  function closeMenu() {
    menuOpen = false;
    menu.classList.remove("is-open");
    menuToggle.setAttribute("aria-expanded", "false");
    menuPanel.hidden = true;
  }

  function openMenu() {
    menuOpen = true;
    menu.classList.add("is-open");
    menuToggle.setAttribute("aria-expanded", "true");
    menuPanel.hidden = false;
  }

  function renderMenu() {
    menu.hidden = view !== "browse";
    if (view !== "browse") {
      closeMenu();
      return;
    }
    var items = categoryItems();
    if (menuPanel.childElementCount !== items.length) {
      menuPanel.innerHTML = "";
      items.forEach(function (item) {
        var button = document.createElement("button");
        button.type = "button";
        button.className = "category-option";
        button.dataset.id = item.id;
        var name = document.createElement("strong");
        var count = document.createElement("span");
        button.appendChild(name);
        button.appendChild(count);
        button.addEventListener("click", function () {
          category = item.id;
          closeMenu();
          closeDetail();
          render();
        });
        menuPanel.appendChild(button);
      });
    }
    var current = items.filter(function (item) { return item.id === category; })[0];
    menuLabel.textContent = current.label;
    menuCount.textContent = String(countFor(current.id));
    menuPanel.querySelectorAll(".category-option").forEach(function (button, index) {
      var item = items[index];
      button.classList.toggle("is-on", item.id === category);
      button.querySelector("strong").textContent = item.label;
      button.querySelector("span").textContent = String(countFor(item.id));
    });
  }

  function ensureGrid() {
    if (main.dataset.grid === category && main.querySelector(".grid")) return;
    main.innerHTML = "";
    var grid = document.createElement("div");
    grid.className = "grid";
    byCategory(category).forEach(function (row) { grid.appendChild(card(row)); });
    var empty = document.createElement("p");
    empty.className = "empty";
    empty.hidden = true;
    empty.textContent = "No characters match.";
    main.appendChild(grid);
    main.appendChild(empty);
    main.dataset.grid = category;
  }

  function applyFilter() {
    var needle = query.trim().toLowerCase();
    var shown = 0;
    main.querySelectorAll(".card").forEach(function (node) {
      var hit = !needle ||
        node.dataset.name.indexOf(needle) !== -1 ||
        node.dataset.series.indexOf(needle) !== -1;
      node.hidden = !hit;
      if (hit) shown += 1;
    });
    var empty = main.querySelector(".empty");
    if (empty) empty.hidden = shown !== 0;
    return shown;
  }

  function renderCategories() {
    main.innerHTML = "";
    delete main.dataset.grid;
    var wrap = document.createElement("div");
    wrap.className = "tiles";
    data.categories.forEach(function (item) {
      var button = document.createElement("button");
      button.type = "button";
      button.className = "tile";
      var name = document.createElement("strong");
      name.textContent = item.label;
      var total = query.trim() ? countFor(item.id) : item.count;
      var count = document.createElement("span");
      count.textContent = total + (total === 1 ? " character" : " characters");
      button.appendChild(name);
      button.appendChild(count);
      button.addEventListener("click", function () {
        category = item.id;
        setView("browse");
      });
      wrap.appendChild(button);
    });
    main.appendChild(wrap);
  }

  function updateStatus(shown) {
    if (view === "categories") {
      status.textContent = "Choose a category";
      return;
    }
    if (query.trim()) {
      status.textContent = shown === 1 ? "1 match" : shown + " matches";
      return;
    }
    status.textContent = data.count + " portraits · Anima and Danbooru";
  }

  function syncDock() {
    document.querySelectorAll(".dock button").forEach(function (button) {
      button.classList.toggle("is-on", button.getAttribute("data-view") === view);
    });
  }

  function setView(next) {
    view = next;
    closeDetail();
    syncDock();
    render();
  }

  function render() {
    renderMenu();
    if (view === "categories") {
      renderCategories();
      updateStatus(0);
      return;
    }
    ensureGrid();
    updateStatus(applyFilter());
  }

  menuToggle.addEventListener("click", function () {
    if (menuOpen) closeMenu();
    else openMenu();
  });
  document.addEventListener("click", function (event) {
    if (menuOpen && !menu.contains(event.target)) closeMenu();
  });
  finder.addEventListener("submit", function (event) { event.preventDefault(); });
  searchInput.addEventListener("input", function () {
    query = searchInput.value;
    clearButton.hidden = query.length === 0;
    if (query.trim() && view !== "browse") {
      view = "browse";
      syncDock();
    }
    render();
  });
  clearButton.addEventListener("click", function () {
    query = "";
    searchInput.value = "";
    clearButton.hidden = true;
    searchInput.focus();
    render();
  });

  document.querySelectorAll(".dock button").forEach(function (button) {
    button.addEventListener("click", function () {
      setView(button.getAttribute("data-view"));
    });
  });

  render();
})();
