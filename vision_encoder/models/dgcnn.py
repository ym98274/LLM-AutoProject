import torch
import torch.nn as nn
import torch.nn.functional as F


def knn(x, k):
    # x: input tensor of shape (B, C, N), where B is batch size, C is number of channels, N is number of points.

    batch_size = x.size(0)
    num_points = x.size(2)

    # Compute squared sum of each point (B, 1, N)
    xx = torch.sum(x ** 2, dim=1, keepdim=True)

    # Compute the inner product matrix (B, N, N)
    inner = -2 * torch.bmm(x.transpose(2, 1), x)  # Use bmm for batch matrix multiplication

    # Pairwise distance matrix: (B, N, N)
    pairwise_distance = -xx - inner - xx.transpose(2, 1)

    # Get the indices of the top-k smallest distances
    idx = pairwise_distance.topk(k=k, dim=-1, largest=False, sorted=False)[
        1]  # Use largest=False to get smallest distances

    return idx


def get_graph_feature(x, k=20, idx=None):
    batch_size = x.size(0)
    num_points = x.size(2)
    x = x.view(batch_size, -1, num_points)
    if idx is None:
        idx = knn(x, k=k)
    device = x.device

    idx_base = torch.arange(0, batch_size, device=device).view(-1, 1, 1) * num_points

    idx = idx + idx_base
    idx = idx.view(-1)

    _, num_dims, _ = x.size()

    x = x.transpose(2, 1).contiguous()
    feature = x.view(batch_size * num_points, -1)[idx, :]
    feature = feature.view(batch_size, num_points, k, num_dims)
    x = x.view(batch_size, num_points, 1, num_dims).repeat(1, 1, k, 1)

    feature = torch.cat((feature - x, x), dim=3).permute(0, 3, 1, 2).contiguous()

    return feature


class DGCNN(nn.Module):
    def __init__(self, k=2, emb_dims=512, dropout=0.5, output_channels=256):
        super(DGCNN, self).__init__()
        self.k = k
        self.emb_dims = emb_dims
        self.dropout = dropout
        self.output_channels = output_channels

        self.in1 = nn.InstanceNorm2d(32)
        self.in2 = nn.InstanceNorm2d(32)
        self.in3 = nn.InstanceNorm2d(64)
        self.in4 = nn.InstanceNorm2d(128)

        self.conv1 = nn.Sequential(nn.Conv2d(8, 32, kernel_size=1, bias=False),
                                   self.in1,
                                   nn.LeakyReLU(negative_slope=0.2))
        self.conv2 = nn.Sequential(nn.Conv2d(64, 32, kernel_size=1, bias=False),
                                   self.in2,
                                   nn.LeakyReLU(negative_slope=0.2))
        self.conv3 = nn.Sequential(nn.Conv2d(64, 64, kernel_size=1, bias=False),
                                   self.in3,
                                   nn.LeakyReLU(negative_slope=0.2))
        self.conv4 = nn.Sequential(nn.Conv2d(128, 128, kernel_size=1, bias=False),
                                   self.in4,
                                   nn.LeakyReLU(negative_slope=0.2))

        self.conv5 = nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=1, bias=False)
        self.conv6 = nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=1, bias=False)

    def forward(self, x):
        batch_size = x.size(0)
        x = get_graph_feature(x, k=self.k)
        x = self.conv1(x)
        x1 = x.max(dim=-1, keepdim=False)[0]

        x = get_graph_feature(x1, k=self.k)
        x = self.conv2(x)
        x2 = x.max(dim=-1, keepdim=False)[0]

        x = get_graph_feature(x2, k=self.k)
        x = self.conv3(x)
        x3 = x.max(dim=-1, keepdim=False)[0]

        x = get_graph_feature(x3, k=self.k)
        x = self.conv4(x)
        x4 = x.max(dim=-1, keepdim=False)[0]

        x = torch.cat((x1, x2, x3, x4), dim=1)

        x = x.unsqueeze(2)
        x = F.leaky_relu(self.conv5(x), negative_slope=0.2)
        x = F.leaky_relu(self.conv6(x), negative_slope=0.2)

        x = F.interpolate(x, size=(50, 50), mode='bilinear', align_corners=True)

        return x