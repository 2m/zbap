<html>
<head></head>
<body>
  <h1>Audio knygų skaityklė</h1>
  <p>Atminties iš viso: <em>{{totalMem}}</em>. Laisva atmintis: <em>{{freeMem}}</em>.</p>
  <table>
  % for item in items:
    <tr>
      <td><p>{{item["name"]}}</p></td>
      <td><p>{{item["tag"]}}</p></td>
      <td>
        % if item["tag"]:
          <a href="remove/{{item["tag"]}}">Atsieti kortelę</a>
        % else:
          <a href="add/{{item["name"]}}">Susieti kortelę</a>
        % end
      </td>
    </tr>
  % end
  </table>
</body>
</html>
