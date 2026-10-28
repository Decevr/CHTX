(function () {
  var data = window.CATALOG;
  var styles = window.STYLES || [];
  var view = "browse";
  var category = "all";
  var title = "";
  var pickingTitles = false;
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

  var TITLE_BY_CATEGORY = {
    marvel: {
      "Black Widow": "Black Widow",
      "Yelena Belova": "Black Widow",
      "Scarlet Witch": "Avengers",
      "Wasp": "Avengers",
      "Maria Hill": "Avengers",
      "Agatha Harkness": "WandaVision",
      "Shuri": "Black Panther",
      "Okoye": "Black Panther",
      "Nakia": "Black Panther",
      "Gamora": "Guardians of the Galaxy",
      "Nebula": "Guardians of the Galaxy",
      "Valkyrie": "Thor",
      "Jane Foster": "Thor",
      "Lady Sif": "Thor",
      "Hela": "Thor",
      "Captain Marvel": "Captain Marvel",
      "Monica Rambeau": "The Marvels",
      "Pepper Potts": "Iron Man",
      "Peggy Carter": "Agent Carter",
      "Sharon Carter": "Captain America",
      "Mary Jane Watson": "Spider-Man",
      "Gwen Stacy": "Spider-Man",
      "Black Cat": "Spider-Man",
      "Silver Sable": "Spider-Man",
      "Silk": "Spider-Man",
      "Spider-Woman": "Spider-Man",
      "Storm": "X-Men",
      "Jean Grey": "X-Men",
      "Rogue": "X-Men",
      "Emma Frost": "X-Men",
      "Psylocke": "X-Men",
      "Magik": "X-Men",
      "Polaris": "X-Men",
      "Dazzler": "X-Men",
      "Kitty Pryde": "X-Men",
      "Jubilee": "X-Men",
      "X-23": "X-Men",
      "Mystique": "X-Men",
      "Domino": "X-Men",
      "Elektra": "Daredevil",
      "She-Hulk": "She-Hulk",
      "Invisible Woman": "Fantastic Four",
      "Medusa": "Inhumans",
      "Crystal": "Inhumans",
      "Jessica Jones": "Jessica Jones",
      "Ms. Marvel": "Ms. Marvel",
      "America Chavez": "Doctor Strange",
      "Daisy Johnson": "Agents of S.H.I.E.L.D.",
      "Ironheart": "Ironheart",
      "Squirrel Girl": "The Unbeatable Squirrel Girl",
      "Mantis": "Guardians of the Galaxy",
      "Frigga": "Thor",
      "Ramonda": "Black Panther",
      "Thena": "Eternals",
      "Amora": "Thor",
      "Clea": "Doctor Strange",
      "Misty Knight": "Luke Cage",
      "Echo": "Hawkeye",
      "Viper": "Captain America"
    },
    dc: {
      "Wonder Woman": "Wonder Woman",
      "Hippolyta": "Wonder Woman",
      "Cheetah": "Wonder Woman",
      "Giganta": "Wonder Woman",
      "Circe": "Wonder Woman",
      "Wonder Girl": "Wonder Woman",
      "Donna Troy": "Wonder Woman",
      "Lois Lane": "Superman",
      "Supergirl": "Superman",
      "Power Girl": "Superman",
      "Livewire": "Superman",
      "Maxima": "Superman",
      "Catwoman": "Batman",
      "Harley Quinn": "Batman",
      "Poison Ivy": "Batman",
      "Batgirl": "Batman",
      "Oracle": "Batman",
      "Batwoman": "Batman",
      "Huntress": "Batman",
      "Cassandra Cain": "Batman",
      "Stephanie Brown": "Batman",
      "Talia al Ghul": "Batman",
      "Lady Shiva": "Batman",
      "Katana": "Batman",
      "Starfire": "Teen Titans",
      "Raven": "Teen Titans",
      "Blackfire": "Teen Titans",
      "Terra": "Teen Titans",
      "Jessica Cruz": "Green Lantern",
      "Carol Ferris": "Green Lantern",
      "Star Sapphire": "Green Lantern",
      "Iris West": "The Flash",
      "Killer Frost": "The Flash",
      "Mera": "Aquaman",
      "Amanda Waller": "Suicide Squad",
      "Enchantress": "Suicide Squad",
      "Black Canary": "Birds of Prey",
      "Hawkgirl": "Justice League",
      "Vixen": "Justice League",
      "Fire": "Justice League",
      "Ice": "Justice League",
      "Zatanna": "Justice League",
      "Stargirl": "Stargirl",
      "Big Barda": "New Gods",
      "Nubia": "Wonder Woman",
      "Atlanna": "Aquaman",
      "Andrea Beaumont": "Batman",
      "Madame Xanadu": "Justice League Dark",
      "Isis": "Black Adam",
      "Jo Mullein": "Green Lantern",
      "Cheshire": "Teen Titans",
      "Silver Banshee": "Superman"
    },
    disney: {
      "Snow White": "Snow White and the Seven Dwarfs",
      "Cinderella": "Cinderella",
      "Aurora": "Sleeping Beauty",
      "Maleficent": "Sleeping Beauty",
      "Ariel": "The Little Mermaid",
      "Belle": "Beauty and the Beast",
      "Jasmine": "Aladdin",
      "Pocahontas": "Pocahontas",
      "Mulan": "Mulan",
      "Tiana": "The Princess and the Frog",
      "Rapunzel": "Tangled",
      "Mother Gothel": "Tangled",
      "Merida": "Brave",
      "Anna": "Frozen",
      "Elsa": "Frozen",
      "Moana": "Moana",
      "Raya": "Raya and the Last Dragon",
      "Namaari": "Raya and the Last Dragon",
      "Asha": "Wish",
      "Mirabel Madrigal": "Encanto",
      "Isabela Madrigal": "Encanto",
      "Luisa Madrigal": "Encanto",
      "Esmeralda": "The Hunchback of Notre Dame",
      "Megara": "Hercules",
      "Jane Porter": "Tarzan",
      "Kida": "Atlantis: The Lost Empire",
      "Giselle": "Enchanted",
      "Alice": "Alice in Wonderland",
      "Wendy Darling": "Peter Pan",
      "Tinker Bell": "Peter Pan",
      "Vanellope von Schweetz": "Wreck-It Ralph",
      "Cruella de Vil": "One Hundred and One Dalmatians",
      "Yzma": "The Emperor's New Groove",
      "Nani Pelekai": "Lilo & Stitch",
      "Lilo Pelekai": "Lilo & Stitch",
      "The Evil Queen": "Snow White and the Seven Dwarfs",
      "Ursula": "The Little Mermaid",
      "Lady Tremaine": "Cinderella",
      "Fairy Godmother": "Cinderella",
      "Queen of Hearts": "Alice in Wonderland",
      "Madam Mim": "The Sword in the Stone",
      "Helga Sinclair": "Atlantis: The Lost Empire",
      "Captain Amelia": "Treasure Planet",
      "Judy Hopps": "Zootopia",
      "Elizabeth Swann": "Pirates of the Caribbean"
    },
    pixar: {
      "Helen Parr": "The Incredibles",
      "Violet Parr": "The Incredibles",
      "Edna Mode": "The Incredibles",
      "Bo Peep": "Toy Story",
      "Jessie": "Toy Story",
      "Gabby Gabby": "Toy Story",
      "Colette Tatou": "Ratatouille",
      "EVE": "WALL-E",
      "Joy": "Inside Out",
      "Sadness": "Inside Out",
      "Disgust": "Inside Out",
      "Riley Andersen": "Inside Out",
      "Ellie Fredricksen": "Up",
      "Ember Lumen": "Elemental",
      "Mei Lee": "Turning Red",
      "Ming Lee": "Turning Red",
      "Dory": "Finding Nemo",
      "Mirage": "The Incredibles",
      "Evelyn Deavor": "The Incredibles",
      "Jill Andersen": "Inside Out",
      "Queen Elinor": "Brave",
      "Mama Imelda": "Coco",
      "Laurel Lightfoot": "Onward",
      "Dorothea Williams": "Soul",
      "Celia Mae": "Monsters, Inc.",
      "Sally Carrera": "Cars",
      "Cinder Lumen": "Elemental"
    },
    pokemon: {
      "Erika": "Pokemon Red and Blue",
      "Sabrina": "Pokemon Red and Blue",
      "Lorelei": "Pokemon Red and Blue",
      "Agatha": "Pokemon Red and Blue",
      "Jasmine": "Pokemon Gold and Silver",
      "Clair": "Pokemon Gold and Silver",
      "Karen": "Pokemon Gold and Silver",
      "Whitney": "Pokemon Gold and Silver",
      "Phoebe": "Pokemon Ruby and Sapphire",
      "Glacia": "Pokemon Ruby and Sapphire",
      "Winona": "Pokemon Ruby and Sapphire",
      "Flannery": "Pokemon Ruby and Sapphire",
      "Courtney": "Pokemon Ruby and Sapphire",
      "Shelly": "Pokemon Ruby and Sapphire",
      "Anabel": "Pokemon Emerald",
      "Lucy": "Pokemon Emerald",
      "Dahlia": "Pokemon Emerald",
      "Cynthia": "Pokemon Diamond and Pearl",
      "Gardenia": "Pokemon Diamond and Pearl",
      "Fantina": "Pokemon Diamond and Pearl",
      "Bertha": "Pokemon Diamond and Pearl",
      "Mars": "Pokemon Diamond and Pearl",
      "Jupiter": "Pokemon Diamond and Pearl",
      "Shauntal": "Pokemon Black and White",
      "Caitlin": "Pokemon Black and White",
      "Elesa": "Pokemon Black and White",
      "Skyla": "Pokemon Black and White",
      "Lenora": "Pokemon Black and White",
      "Professor Juniper": "Pokemon Black and White",
      "Diantha": "Pokemon X and Y",
      "Malva": "Pokemon X and Y",
      "Drasna": "Pokemon X and Y",
      "Viola": "Pokemon X and Y",
      "Olympia": "Pokemon X and Y",
      "Valerie": "Pokemon X and Y",
      "Alexa": "Pokemon X and Y",
      "Lusamine": "Pokemon Sun and Moon",
      "Plumeria": "Pokemon Sun and Moon",
      "Wicke": "Pokemon Sun and Moon",
      "Mina": "Pokemon Sun and Moon",
      "Olivia": "Pokemon Sun and Moon",
      "Kahili": "Pokemon Sun and Moon",
      "Nessa": "Pokemon Sword and Shield",
      "Bea": "Pokemon Sword and Shield",
      "Melony": "Pokemon Sword and Shield",
      "Oleana": "Pokemon Sword and Shield",
      "Sonia": "Pokemon Sword and Shield",
      "Opal": "Pokemon Sword and Shield",
      "Professor Magnolia": "Pokemon Sword and Shield",
      "Geeta": "Pokemon Scarlet and Violet",
      "Rika": "Pokemon Scarlet and Violet",
      "Tulip": "Pokemon Scarlet and Violet",
      "Dendra": "Pokemon Scarlet and Violet",
      "Ryme": "Pokemon Scarlet and Violet",
      "Iono": "Pokemon Scarlet and Violet",
      "Katy": "Pokemon Scarlet and Violet",
      "Miriam": "Pokemon Scarlet and Violet",
      "Raifort": "Pokemon Scarlet and Violet",
      "Briar": "Pokemon Scarlet and Violet",
      "Jessie": "Pokemon the Series",
      "Cassidy": "Pokemon the Series",
      "Zinnia": "Pokemon Omega Ruby and Alpha Sapphire",
      "Professor Burnet": "Pokemon Sun and Moon",
      "Ariana": "Pokemon HeartGold and SoulSilver"
    }
  };

  function titleFor(row) {
    var table = TITLE_BY_CATEGORY[row.category];
    if (table && table[row.name]) return table[row.name];
    return row.series;
  }

  function titlesFor(categoryId) {
    var seen = {};
    var list = [];
    data.characters.forEach(function (row) {
      if (row.category !== categoryId) return;
      var name = titleFor(row);
      if (!seen[name]) {
        seen[name] = 0;
        list.push(name);
      }
      seen[name] += 1;
    });
    list.sort(function (a, b) { return a.localeCompare(b); });
    return list.map(function (name) { return { name: name, count: seen[name] }; });
  }

  function byCategory(id) {
    if (id === "all") return data.characters;
    return data.characters.filter(function (row) { return row.category === id; });
  }

  function bySelection() {
    return data.characters.filter(function (row) {
      if (category !== "all" && row.category !== category) return false;
      if (title && titleFor(row) !== title) return false;
      return true;
    });
  }

  function labelFor(id) {
    var found = data.categories.filter(function (row) { return row.id === id; })[0];
    return found ? found.label : id;
  }

  function matches(row, needle) {
    if (!needle) return true;
    return row.name.toLowerCase().indexOf(needle) !== -1 ||
      row.series.toLowerCase().indexOf(needle) !== -1 ||
      titleFor(row).toLowerCase().indexOf(needle) !== -1;
  }

  function countFor(id, titleName) {
    var needle = query.trim().toLowerCase();
    var total = 0;
    data.characters.forEach(function (row) {
      if (id !== "all" && row.category !== id) return;
      if (titleName && titleFor(row) !== titleName) return;
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
    var work = titleFor(row);
    detail.querySelector(".meta").textContent = work === row.series
      ? row.series + " · " + labelFor(row.category)
      : work + " · " + row.series + " · " + labelFor(row.category);
    detail.querySelector("#positive").textContent = row.positive;
    detail.querySelector("#booru").textContent = row.booru || "";
    detail.querySelector(".note").textContent = data.settings.note;
    detail.querySelector("#back").addEventListener("click", closeDetail);
    detail.querySelector("#copy-positive").addEventListener("click", function () { copyText(row.positive); });
    detail.querySelector("#copy-booru").addEventListener("click", function () { copyText(row.booru || ""); });
  }

  function openStyleDetail(index) {
    var row = styles[index];
    detail.hidden = false;
    detail.scrollTop = 0;
    detail.innerHTML =
      '<div class="detail-bar"><button type="button" class="back" id="back">Back</button></div>' +
      '<img class="portrait" alt="">' +
      '<div class="detail-copy"><h2></h2><p class="meta">Example</p></div>' +
      '<article class="prompt"><h3>Prompt</h3><p id="style-prompt"></p><button type="button" class="copy" id="copy-style">Copy prompt</button></article>';
    detail.querySelector(".portrait").src = row.image;
    detail.querySelector("h2").textContent = row.name;
    detail.querySelector("#style-prompt").textContent = row.prompt;
    detail.querySelector("#back").addEventListener("click", closeDetail);
    detail.querySelector("#copy-style").addEventListener("click", function () { copyText(row.prompt); });
  }

  function closeDetail() {
    detail.hidden = true;
    detail.innerHTML = "";
  }

  function copyText(text) {
    if (window.CHTX && window.CHTX.copy) {
      window.CHTX.copy(text);
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
    button.dataset.title = titleFor(row).toLowerCase();
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

  function menuItems() {
    var items = [{ kind: "all", id: "all", label: "All", category: "all", title: "" }];
    data.categories.forEach(function (cat) {
      items.push({ kind: "category", id: cat.id, label: cat.label, category: cat.id, title: "" });
      titlesFor(cat.id).forEach(function (entry) {
        items.push({
          kind: "title",
          id: cat.id + "::" + entry.name,
          label: entry.name,
          category: cat.id,
          title: entry.name
        });
      });
    });
    return items;
  }

  function itemSelected(item) {
    if (item.kind === "all") return category === "all";
    if (item.kind === "category") return category === item.category && !title;
    return category === item.category && title === item.title;
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
    var items = menuItems();
    var signature = items.map(function (item) { return item.id; }).join("|");
    if (menuPanel.dataset.signature !== signature) {
      menuPanel.innerHTML = "";
      items.forEach(function (item) {
        var button = document.createElement("button");
        button.type = "button";
        button.className = item.kind === "title" ? "category-option sub" : "category-option";
        button.dataset.id = item.id;
        var name = document.createElement("strong");
        var count = document.createElement("span");
        button.appendChild(name);
        button.appendChild(count);
        button.addEventListener("click", function () {
          category = item.category;
          title = item.title;
          pickingTitles = false;
          closeMenu();
          closeDetail();
          render();
        });
        menuPanel.appendChild(button);
      });
      menuPanel.dataset.signature = signature;
    }
    var current = items.filter(itemSelected)[0] || items[0];
    menuLabel.textContent = current.label;
    menuCount.textContent = String(countFor(current.category, current.title));
    menuPanel.querySelectorAll(".category-option").forEach(function (button, index) {
      var item = items[index];
      button.classList.toggle("is-on", itemSelected(item));
      button.querySelector("strong").textContent = item.label;
      button.querySelector("span").textContent = String(countFor(item.category, item.title));
    });
  }

  function appendGroup(parent, heading, rows) {
    var section = document.createElement("section");
    section.className = "group";
    var name = document.createElement("h3");
    name.textContent = heading;
    var grid = document.createElement("div");
    grid.className = "grid";
    rows.slice().sort(function (a, b) { return a.name.localeCompare(b.name); }).forEach(function (row) {
      grid.appendChild(card(row));
    });
    section.appendChild(name);
    section.appendChild(grid);
    parent.appendChild(section);
  }

  function ensureGrid() {
    var key = category + "\n" + title;
    if (main.dataset.grid === key && main.querySelector(".groups, .grid")) return;
    main.innerHTML = "";
    var rows = bySelection();
    if (category === "all") {
      var grid = document.createElement("div");
      grid.className = "grid";
      rows.forEach(function (row) { grid.appendChild(card(row)); });
      main.appendChild(grid);
    } else if (title) {
      appendGroup(main, title, rows);
    } else {
      var groups = {};
      var order = [];
      rows.forEach(function (row) {
        var name = titleFor(row);
        if (!groups[name]) {
          groups[name] = [];
          order.push(name);
        }
        groups[name].push(row);
      });
      order.sort(function (a, b) { return a.localeCompare(b); });
      order.forEach(function (name) { appendGroup(main, name, groups[name]); });
    }
    var empty = document.createElement("p");
    empty.className = "empty";
    empty.hidden = true;
    empty.textContent = "No characters match.";
    main.appendChild(empty);
    main.dataset.grid = key;
  }

  function applyFilter() {
    var needle = query.trim().toLowerCase();
    var shown = 0;
    main.querySelectorAll(".card").forEach(function (node) {
      var hit = !needle ||
        node.dataset.name.indexOf(needle) !== -1 ||
        node.dataset.series.indexOf(needle) !== -1 ||
        node.dataset.title.indexOf(needle) !== -1;
      node.hidden = !hit;
      if (hit) shown += 1;
    });
    main.querySelectorAll(".group").forEach(function (section) {
      var visible = section.querySelectorAll(".card:not([hidden])").length;
      section.hidden = visible === 0;
    });
    var empty = main.querySelector(".empty");
    if (empty) empty.hidden = shown !== 0;
    return shown;
  }

  function renderCategories() {
    main.innerHTML = "";
    delete main.dataset.grid;
    if (pickingTitles && category !== "all") {
      var back = document.createElement("button");
      back.type = "button";
      back.className = "title-back";
      back.textContent = "All categories";
      back.addEventListener("click", function () {
        pickingTitles = false;
        category = "all";
        title = "";
        render();
      });
      main.appendChild(back);
      var heading = document.createElement("p");
      heading.className = "title-heading";
      heading.textContent = labelFor(category);
      main.appendChild(heading);
      var titles = document.createElement("div");
      titles.className = "tiles";
      titlesFor(category).forEach(function (entry) {
        var button = document.createElement("button");
        button.type = "button";
        button.className = "tile title-tile";
        var name = document.createElement("strong");
        name.textContent = entry.name;
        var total = query.trim() ? countFor(category, entry.name) : entry.count;
        var count = document.createElement("span");
        count.textContent = total + (total === 1 ? " character" : " characters");
        button.appendChild(name);
        button.appendChild(count);
        button.addEventListener("click", function () {
          title = entry.name;
          pickingTitles = false;
          setView("browse");
        });
        titles.appendChild(button);
      });
      main.appendChild(titles);
      return;
    }
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
        title = "";
        pickingTitles = true;
        render();
      });
      wrap.appendChild(button);
    });
    main.appendChild(wrap);
  }

  function renderStyles() {
    main.innerHTML = "";
    delete main.dataset.grid;
    var needle = query.trim().toLowerCase();
    var grid = document.createElement("div");
    grid.className = "grid";
    var shown = 0;
    styles.forEach(function (row, index) {
      if (needle && row.name.toLowerCase().indexOf(needle) === -1) return;
      shown += 1;
      var button = document.createElement("button");
      button.type = "button";
      button.className = "card";
      var image = document.createElement("img");
      image.alt = "";
      image.loading = "lazy";
      image.src = row.image;
      var copy = document.createElement("div");
      var heading = document.createElement("h2");
      heading.textContent = row.name;
      var series = document.createElement("p");
      series.textContent = "Example";
      copy.appendChild(heading);
      copy.appendChild(series);
      button.appendChild(image);
      button.appendChild(copy);
      button.addEventListener("click", function () { openStyleDetail(index); });
      grid.appendChild(button);
    });
    main.appendChild(grid);
    var empty = document.createElement("p");
    empty.className = "empty";
    empty.hidden = shown !== 0;
    empty.textContent = "No styles match.";
    main.appendChild(empty);
    status.textContent = shown === 1 ? "1 style" : shown + " styles";
  }

  function updateStatus(shown) {
    if (view === "categories") {
      status.textContent = pickingTitles && category !== "all" ? "Choose a title" : "Choose a category";
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
    if (next !== "categories") pickingTitles = false;
    closeDetail();
    syncDock();
    render();
  }

  function render() {
    syncDock();
    searchInput.placeholder = view === "styles" ? "Search a style" : "Search a character";
    renderMenu();
    if (view === "categories") {
      renderCategories();
      updateStatus(0);
      return;
    }
    if (view === "styles") {
      renderStyles();
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
    if (query.trim() && view === "categories") {
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
