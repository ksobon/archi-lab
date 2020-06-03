PUT beat-2020-cad-1.0.0-000001/_settings
{
  "index": {
    "blocks": {
      "read_only_allow_delete": "false"
    }
  }
}

PUT _all/_settings
{
  "index": {
    "blocks": {
      "read_only_allow_delete": null
    }
  }
}

PUT _cluster/settings
{
  "transient": {
    "cluster": {
      "routing": {
        "allocation": {
          "disk": {
            "threshold_enabled": true
          }
        }
      }
    }
  }
}

GET _nodes
GET _cluster/stats/nodes/tiebreaker-0000000039
GET _cluster/stats/nodes/instance-0000000040
GET _cluster/stats/nodes/instance-0000000039
GET _cluster/stats/nodes/instance-0000000038

GET _cluster/stats/nodes/instance-0000000037
GET _cluster/stats/nodes/instance-0000000036


GET _ilm/policy/metricbeat-max40Gb-noMaxAge

GET _cluster/health/metricbeat-2020-7.4.2

GET _cat/shards

GET /_nodes/instance-0000000040/_all

GET .kibana/_search
{
  "_source": ["index-pattern.title"],
  "query": {
    "bool": {
      "must": [
        {"match": {"index-pattern.title": "*revit*"}},
        {"match": {"type": "index-pattern"}}
        ]
    }
  }
}
