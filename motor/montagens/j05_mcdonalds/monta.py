import subprocess
C='/mnt/user-data/uploads/Downloads/05-11_mcdonalds/clipes/'
src={1:'clipe_01',2:'clipe_02',3:'clipe_03',4:'clipe_04_corrigido',5:'clipe_05_corrigido',6:'clipe_06',7:'clipe_07_corrigido',8:'clipe_08',10:'clipe_10',11:'clipe_11',12:'clipe_12',13:'clipe_13',14:'clipe_14'}
cut=[0,6.2,11.2,16.9,20.8,24.8,28.6,34.8,38.6,43.4,49.2,52.4,57.1,62.9,68.6]
L=open('lista.txt','w')
for i in range(14):
    n=i+1; d=cut[i+1]-cut[i]; out=f's{n:02d}.mp4'
    if n in src:
        k=max(1.0,d/5.0)
        vf=f"setpts=(PTS-STARTPTS)*{k:.4f},fps=30,scale=1080:1920:flags=lanczos,setsar=1,tpad=stop_mode=clone:stop_duration=1"
        cmd=["ffmpeg","-loglevel","error","-y","-ss","0.1","-i",C+src[n]+'.mp4',"-an","-vf",vf]
    else:
        fr=int(d*30)
        vf=f"scale=2160:-2,zoompan=z='1+0.10*on/{fr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={fr}:s=1080x1920:fps=30,setsar=1"
        cmd=["ffmpeg","-loglevel","error","-y","-i",'/mnt/user-data/outputs/pastas/05-11_mcdonalds/fotos/09.jpg',"-vf",vf]
    subprocess.run(cmd+["-t",f"{d:.3f}","-c:v","libx264","-preset","veryfast","-crf","14","-pix_fmt","yuv420p",out],check=True)
    L.write(f"file '{out}'\n")
L.close()
