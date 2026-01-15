
# lidaplot (CCP-ready package)

Run in CCP (Python 3):

```
git clone <your-repo>
cd lidaplot
pip install -r requirements.txt
python3 main.py --obs_site POT --obs_date_min 2025-06-13 --obs_date_max 2025-06-13   --obs_hour_min 21:00 --obs_hour_max 23:00 --panel 5p --basepath /ccp_data
```

Outputs:
- `/ccp_data/tmp`: downloaded ZIPs
- `/ccp_data/output`: extracted NetCDF
- `/ccp_data/plots`: PNG figures
