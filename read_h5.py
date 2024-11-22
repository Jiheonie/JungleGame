import h5py

# Mở file HDF5
with h5py.File('agents/policy_gradient_agent.hdf5', 'r') as hdf:
  # In danh sách các nhóm (groups) ở cấp cao nhất
  print(list(hdf.keys()))
  group = hdf['model']
  print(list(group.keys()))
  # Đọc thuộc tính của một nhóm hoặc dataset
  attrs = group['kerasmodel'].attrs
  for attr_name, attr_value in attrs.items():
    print(f"{attr_name}: {attr_value}")