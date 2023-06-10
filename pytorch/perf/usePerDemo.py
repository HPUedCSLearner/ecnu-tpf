import torch
from torchvision.models import resnet18

with torch.autograd.profiler.profile(enabled=True, use_cuda=True, record_shapes=False, profile_memory=False) as prof:
    x = torch.rand(3,3)
    x.fill_(999)
print(prof.table())
prof.export_chrome_trace('./profile.json')

with torch.autograd.profiler.profile(enabled=True, use_cuda=True, record_shapes=False, profile_memory=False) as prof:
    model = resnet18(pretrained=False)
    device = torch.device('cpu')
    model.eval()
    model.to(device)
    dump_input = torch.ones(1,3,224,224).to(device)
# print(prof.table())
print(prof.key_averages().table(sort_by="self_cpu_time_total", row_limit=100))