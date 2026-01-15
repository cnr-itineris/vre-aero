
# lidaplot (CCP-ready v2)

Run in CCP (Python 3):

```
pip install -r requirements.txt
python3 main.py --obs_site POT --obs_date_min 2025-06-13 --obs_date_max 2025-06-13   --obs_hour_min 21:00 --obs_hour_max 23:00 --panel 5p --basepath /ccp_data
```

Troubleshooting (verbose):
```
DEBUG=1 python3 _get_data.py 2025-06-13 2025-06-13 21:00 23:00 POT /ccp_data
```
