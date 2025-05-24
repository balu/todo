import sqlite3
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)
DB = 'todos.db'

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>TODO</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {
      font-family: 'Fira Mono', 'Consolas', 'Menlo', 'Monaco', monospace;
      background: #f0f0f0;
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    .container {
      max-width: 650px;
      margin: 24px auto;
      padding: 16px;
      background: #ffffff;
      border-radius: 12px;
      box-shadow: 0 2px 8px #0001;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }
    form, div#appt-fields, div#task-fields {
      display: flex;
      flex-direction: column;
      gap: 12px;
      align-items: stretch;
      justify-content: flex-start;
    }
    form label {
      font-size: 0.98em;
      color: #595959;
      margin-bottom: 2px;
      margin-top: 8px;
    }
    form input, form select {
      font-family: inherit;
      font-size: 1em;
      padding: 4px 8px;
      border: 1px solid #9f9f9f;
      border-radius: 5px;
      min-width: 0;
      background: #f0f0f0;
      line-height: 1.2em;
      height: 2.2em;
      box-sizing: border-box;
      width: 100%;
      margin-bottom: 0;
    }
    form button {
      font-family: inherit;
      font-size: 1em;
      padding: 8px 16px;
      background: #222222;
      color: #ffffff;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      transition: background 0.2s;
      margin-top: 12px;
      width: 100%;
    }
    form button:hover {
      background: #444444;
    }
    ul.todolist {
      list-style: none;
      padding: 0;
      margin: 0;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .todo-item {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      background: #f0f0f0;
      border-radius: 6px;
      padding: 12px;
      gap: 10px;
    }
    .todo-desc {
      flex: 2 1 1.2em;
      font-size: 1em;
      word-break: break-word;
    }
    .todo-times {
      flex: 2 1 1.2em;
      font-size: 0.95em;
      color: #193668;
      text-align: right;
      display: flex;
      flex-direction: column;
      gap: 1px;
      align-items: flex-end;
    }
    .todo-actions {
      display: flex;
      gap: 6px;
      flex: 0 0 auto;
    }
    .todo-actions button {
      font-family: inherit;
      font-size: 0.97em;
      padding: 5px 14px;
      border-radius: 4px;
      border: none;
      cursor: pointer;
      background: #eee;
      color: #222;
      transition: background 0.18s;
    }
    .todo-actions button.nope { background: #ff6b6b; }
    .todo-actions button.nope:hover { background: #ff3b3b; }
    .todo-actions button.wait { background: #ffd93d; }
    .todo-actions button.wait:hover { background: #ffc300; }
    .todo-actions button.done { background: #51cf66; }
    .todo-actions button.done:hover { background: #38b349; }
    .todo-actions button.todo { background: #4d96ff; }
    .todo-actions button.todo:hover { background: #256dff; }
    @media (max-width: 600px) {
      .container {
        max-width: 97vw;
        padding: 8px;
      }
      .todo-item {
        flex-direction: column;
        align-items: stretch;
        gap: 8px;
      }
      .todo-times {
        align-items: flex-start;
        text-align: left;
      }
    }

    @media (prefers-color-scheme: dark) {
      body {
        background: #111;
        color: white;
      }
     .container {
        background: #262626;
      }
      form label {
        color: #eee;
      }
      form input, form select {
        background: #3b3b3b;
        color: white;
      }
      ::placeholder {
        color: #ccc;
      }
      form button {
        background: #3b3b3b;
        color: #fff;
      }
      form button:hover {
        background: #525252;
      }
      .todo-item {
        background: #3b3b3b;
      }
      .todo-times {
        color: #ddd;
      }
      .todo-actions button {
        background: #3b3b3b;
        color: #fff;
      }
      .todo-actions button.nope { background: #9b2318; }
      .todo-actions button.nope:hover { background: #c52f21; color: #fff; }
      .todo-actions button.wait { background: #5b5300; }
      .todo-actions button.wait:hover { background: #756b00; color: #fff; }
      .todo-actions button.done { background: #265e09; }
      .todo-actions button.done:hover { background: #33790f; color: #fff; }
      .todo-actions button.todo { background: #184eb8; }
      .todo-actions button.todo:hover { background: #2060df; color: #fff; }
    }
  </style>
  <script>
    function onTypeChange() {
      var type = document.getElementById("type").value;
      document.getElementById("appt-fields").style.display = type === "APPOINTMENT" ? "flex" : "none";
      document.getElementById("task-fields").style.display = type === "TASK" ? "flex" : "none";
    }
    window.addEventListener('DOMContentLoaded', function() {
      onTypeChange();
    });
  </script>
</head>
<body>
  <div class="container">
    <details>
      <summary>Add a task or an appointment</summary>
      <form id="todo-form" method="POST" action="{{ url_for('add') }}" autocomplete="off">
        <label for="type">Type</label>
        <select name="type" id="type" onchange="onTypeChange()">
          <option value="TASK">TASK</option>
          <option value="APPOINTMENT">APPOINTMENT</option>
        </select>
        <label for="desc">Description</label>
        <input type="text" name="desc" id="desc" placeholder="A short description" required maxlength="100">
        <div id="task-fields" style="display:none;">
          <label for="task_scheduled">Scheduled</label>
          <input type="datetime-local" name="task_scheduled" id="task_scheduled" placeholder="Scheduled start">
          <label for="task_deadline">Deadline</label>
          <input type="datetime-local" name="task_deadline" id="task_deadline" placeholder="Deadline">
        </div>
        <div id="appt-fields" style="display:none;">
          <label for="appt_begin">Begin</label>
          <input type="datetime-local" name="appt_begin" id="appt_begin" placeholder="Begin time">
          <label for="appt_end">End</label>
          <input type="datetime-local" name="appt_end" id="appt_end" placeholder="End time">
        </div>
        <button type="submit">ADD</button>
      </form>
    </details>
    <ul class="todolist">
      {% for t in todos %}
        <li class="todo-item">
          <span class="todo-desc">
            [{{ t['item_type'][0] }}] {{ t['description'] }}
          </span>
          <span class="todo-times">
            {% if t['item_type'] == 'APPOINTMENT' %}
              <span>B: {{ t['begin_time_fmt'] }}</span>
              <span>E:   {{ t['end_time_fmt'] }}</span>
            {% else %}
              <span>S: {{ t['scheduled_time_fmt'] }}</span>
              <span>D:  {{ t['deadline_fmt'] }}</span>
            {% endif %}
          </span>
          <span class="todo-actions">
            {% if t['state'] == 'TODO' %}
              <form method="POST" action="{{ url_for('update', id=t['id']) }}" style="display:inline">
                <input type="hidden" name="state" value="DONE">
                <button class="done" title="DONE" type="submit">DONE</button>
              </form>
              <form method="POST" action="{{ url_for('update', id=t['id']) }}" style="display:inline">
                <input type="hidden" name="state" value="NOPE">
                <button class="nope" title="NOPE" type="submit">NOPE</button>
              </form>
              <form method="POST" action="{{ url_for('update', id=t['id']) }}" style="display:inline">
                <input type="hidden" name="state" value="WAIT">
                <button class="wait" title="WAIT" type="submit">WAIT</button>
              </form>
            {% elif t['state'] == 'WAIT' %}
              <form method="POST" action="{{ url_for('update', id=t['id']) }}" style="display:inline">
                <input type="hidden" name="state" value="DONE">
                <button class="done" title="DONE" type="submit">DONE</button>
              </form>
              <form method="POST" action="{{ url_for('update', id=t['id']) }}" style="display:inline">
                <input type="hidden" name="state" value="NOPE">
                <button class="nope" title="NOPE" type="submit">NOPE</button>
              </form>
              <form method="POST" action="{{ url_for('update', id=t['id']) }}" style="display:inline">
                <input type="hidden" name="state" value="TODO">
                <button class="todo" title="TODO" type="submit">TODO</button>
              </form>
            {% endif %}
          </span>
        </li>
      {% else %}
        <li style="color:#aaa; font-size:1em; text-align:center;">Nothing to do. Yay!</li>
      {% endfor %}
    </ul>
  </div>
</body>
</html>
"""

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    # item_type: APPOINTMENT or TASK
    # For APPOINTMENT: begin_time, end_time used
    # For TASK: scheduled_time, deadline used
    c.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_type TEXT NOT NULL CHECK(item_type IN ('APPOINTMENT', 'TASK')),
            description TEXT NOT NULL,
            begin_time TEXT,
            end_time TEXT,
            scheduled_time TEXT,
            deadline TEXT,
            state TEXT NOT NULL CHECK(state IN ('TODO', 'WAIT', 'DONE', 'NOPE'))
        )
    ''')
    conn.commit()
    conn.close()

def get_todos():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('''
        SELECT * FROM todos WHERE state IN ("TODO", "WAIT")
        ORDER BY 
          CASE WHEN item_type='APPOINTMENT' THEN begin_time
               WHEN item_type='TASK' THEN scheduled_time
          END ASC
    ''')
    todos = [dict(row) for row in c.fetchall()]
    for t in todos:
        # Format times nicely
        from datetime import datetime
        def fmt(dtstr):
            if not dtstr: return ""
            try:
                return datetime.fromisoformat(dtstr).strftime("%a, %b %d, %H:%M")
            except Exception:
                return dtstr
        if t['item_type'] == 'APPOINTMENT':
            t['begin_time_fmt'] = fmt(t['begin_time'])
            t['end_time_fmt'] = fmt(t['end_time'])
        else:
            t['scheduled_time_fmt'] = fmt(t['scheduled_time'])
            t['deadline_fmt'] = fmt(t['deadline'])
    conn.close()
    return todos

@app.route("/", methods=["GET"])
def index():
    todos = get_todos()
    return render_template_string(HTML, todos=todos)

@app.route("/add", methods=["POST"])
def add():
    typ = request.form.get("type")
    desc = request.form.get("desc", "").strip()
    if typ == "APPOINTMENT":
        begin = request.form.get("appt_begin")
        end = request.form.get("appt_end")
        scheduled = deadline = None
    elif typ == "TASK":
        scheduled = request.form.get("task_scheduled")
        deadline = request.form.get("task_deadline")
        begin = end = None
    else:
        return redirect(url_for("index"))
    if desc and ((typ == "APPOINTMENT" and begin and end) or (typ == "TASK" and scheduled and deadline)):
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute('''
            INSERT INTO todos (item_type, description, begin_time, end_time, scheduled_time, deadline, state)
            VALUES (?, ?, ?, ?, ?, ?, "TODO")
        ''', (typ, desc, begin, end, scheduled, deadline))
        conn.commit()
        conn.close()
    return redirect(url_for("index"))

@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    new_state = request.form.get("state")
    if new_state in ("TODO", "WAIT", "DONE", "NOPE"):
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute('UPDATE todos SET state=? WHERE id=?', (new_state, id))
        conn.commit()
        conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
