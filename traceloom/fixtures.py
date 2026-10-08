from .models import Run, Span


def _span(run,i,kind,name,status="ok",milestone=None,cost=.0002):
    return Span(run,f"{run}-s{i}",i,kind,name,i*100,80,120,cost,status,milestone,{"query":name},{"recorded":True})


def sample_runs() -> list[Run]:
    return [
      Run("run-001","Find and summarize policy",True,(_span("run-001",0,"model","plan",milestone="planned"),_span("run-001",1,"tool","search",milestone="source_found"),_span("run-001",2,"model","answer",milestone="completed"))),
      Run("run-002","Resolve shipment exception",False,(_span("run-002",0,"model","plan",milestone="planned"),_span("run-002",1,"tool","lookup"),_span("run-002",2,"tool","reroute"),_span("run-002",3,"tool","notify"),_span("run-002",4,"model","replan")),"infinite_loop"),
      Run("run-003","Fetch weather",False,(_span("run-003",0,"model","plan",milestone="planned"),_span("run-003",1,"tool","weather",status="timeout")),"timeout"),
      Run("run-004","Book restricted item",False,(_span("run-004",0,"model","plan",milestone="planned"),_span("run-004",1,"model","answer",status="refused")),"refusal"),
      Run("run-005","Research options",True,(_span("run-005",0,"model","plan",milestone="planned"),_span("run-005",1,"tool","search"),_span("run-005",2,"tool","search"),_span("run-005",3,"tool","search",milestone="source_found"),_span("run-005",4,"model","answer",milestone="completed"))),
    ]

