(function () {
  var data = window.CATALOG;
  var view = "browse";
  var category = "all";
  var query = "";
  var main = document.getElementById("main");
  var chips = document.getElementById("chips");
  var detail = document.getElementById("detail");
  var toast = document.getElementById("toast");

  document.getElementById("lede").textContent =
    data.count + " character portraits, with a sentence prompt and Danbooru tags.";

  function byCategory(id) {
    if (id === "all") return data.characters;
    return data.characters.filter(function (row) { return row.category === id; });
  }

  function labelFor(id) {
    var found = data.categories.filter(function (row) { return row.id === id; })[0];
    return found ? found.label : id;
  }

  function openDetail(index) {
    var row = data.characters[index];
    detail.hidden = false;
    detail.scrollTop = 0;
    detail.innerHTML =
      '<div class="detail-bar"><button type="button" class="back" id="back">Back</button></div>' +
      '<img class="portrait" alt="">' +
      '<div class="detail-copy"><h2></h2><p class="meta"></p></div>' +
      '<article class="prompt"><h3>Positive</h3><p id="positive"></p><button type="button" class="copy" id="copy-positive">Copy positive</button></article>' +
      '<article class="prompt"><h3>Negative</h3><p id="negative"></p><button type="button" class="copy" id="copy-negative">Copy negative</button></article>' +
      '<article class="prompt"><h3>Danbooru / Gelbooru</h3><p id="booru"></p><button type="button" class="copy" id="copy-booru">Copy tags</button></article>' +
      '<article class="prompt"><h3>Danbooru / Gelbooru negative</h3><p id="booru-negative"></p><button type="button" class="copy" id="copy-booru-negative">Copy tag negative</button></article>' +
      '<p class="note"></p>';
    detail.querySelector(".portrait").src = row.image;
    detail.querySelector("h2").textContent = row.name;
    detail.querySelector(".meta").textContent = row.series + " · " + labelFor(row.category);
    detail.querySelector("#positive").textContent = row.positive;
    detail.querySelector("#negative").textContent = row.negative;
    detail.querySelector("#booru").textContent = row.booru || "";
    detail.querySelector("#booru-negative").textContent = row.booru_negative || "";
    detail.querySelector(".note").textContent = data.settings.note;
    detail.querySelector("#back").addEventListener("click", closeDetail);
    detail.querySelector("#copy-positive").addEventListener("click", function () { copyText(row.positive); });
    detail.querySelector("#copy-negative").addEventListener("click", function () { copyText(row.negative); });
    detail.querySelector("#copy-booru").addEventListener("click", function () { copyText(row.booru || ""); });
    detail.querySelector("#copy-booru-negative").addEventListener("click", function () { copyText(row.booru_negative || ""); });
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

  function renderChips() {
    chips.hidden = view !== "browse";
    if (view !== "browse") return;
    chips.innerHTML = "";
    var items = [{ id: "all", label: "All", count: data.count }].concat(data.categories);
    items.forEach(function (item) {
      var button = document.createElement("button");
      button.type = "button";
      button.className = "chip" + (item.id === category ? " is-on" : "");
      button.textContent = item.label + " " + item.count;
      button.addEventListener("click", function () {
        category = item.id;
        render();
      });
      chips.appendChild(button);
    });
  }

  function renderBrowse() {
    var grid = document.createElement("div");
    grid.className = "grid";
    byCategory(category).forEach(function (row) { grid.appendChild(card(row)); });
    main.appendChild(grid);
  }

  function renderCategories() {
    var wrap = document.createElement("div");
    wrap.className = "tiles";
    data.categories.forEach(function (item) {
      var button = document.createElement("button");
      button.type = "button";
      button.className = "tile";
      var name = document.createElement("strong");
      name.textContent = item.label;
      var count = document.createElement("span");
      count.textContent = item.count + " characters";
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

  function renderSearch() {
    var wrap = document.createElement("div");
    wrap.className = "search";
    var input = document.createElement("input");
    input.type = "search";
    input.placeholder = "Search characters or series";
    input.value = query;
    input.setAttribute("enterkeyhint", "search");
    var results = document.createElement("div");
    results.className = "results";
    function paint() {
      results.innerHTML = "";
      var needle = query.trim().toLowerCase();
      var rows = data.characters.filter(function (row) {
        if (!needle) return false;
        return row.name.toLowerCase().indexOf(needle) !== -1 ||
          row.series.toLowerCase().indexOf(needle) !== -1;
      }).slice(0, 40);
      if (!needle) {
        var hint = document.createElement("p");
        hint.className = "empty";
        hint.textContent = "Search by character or series.";
        results.appendChild(hint);
        return;
      }
      if (!rows.length) {
        var empty = document.createElement("p");
        empty.className = "empty";
        empty.textContent = "No matches.";
        results.appendChild(empty);
        return;
      }
      rows.forEach(function (row) {
        var button = document.createElement("button");
        button.type = "button";
        button.className = "result";
        var image = document.createElement("img");
        image.alt = "";
        image.src = row.image;
        var copy = document.createElement("div");
        var title = document.createElement("strong");
        title.textContent = row.name;
        var series = document.createElement("span");
        series.textContent = row.series;
        copy.appendChild(title);
        copy.appendChild(series);
        button.appendChild(image);
        button.appendChild(copy);
        button.addEventListener("click", function () {
          openDetail(data.characters.indexOf(row));
        });
        results.appendChild(button);
      });
    }
    input.addEventListener("input", function () {
      query = input.value;
      paint();
    });
    wrap.appendChild(input);
    wrap.appendChild(results);
    main.appendChild(wrap);
    paint();
    input.focus();
  }

  function setView(next) {
    view = next;
    document.querySelectorAll(".dock button").forEach(function (button) {
      button.classList.toggle("is-on", button.getAttribute("data-view") === view);
    });
    render();
  }

  function render() {
    closeDetail();
    main.innerHTML = "";
    renderChips();
    if (view === "categories") renderCategories();
    else if (view === "search") renderSearch();
    else renderBrowse();
  }

  document.querySelectorAll(".dock button").forEach(function (button) {
    button.addEventListener("click", function () {
      setView(button.getAttribute("data-view"));
    });
  });

  render();
})();
