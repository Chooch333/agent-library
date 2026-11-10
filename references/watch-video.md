# Watching a video in a post

Read when a message carries an X or Instagram link whose post has a video and the chat needs what the video shows. Claude cannot take a video file, but it can open the post in a browser on Charles's PC, jump through the video and read stills. Never tell Charles a video can't be seen, and never ask him to describe it, before these steps. YouTube links: `references/youtube-transcript.md` first (the words); use this only when the picture matters (not yet tested on YouTube).

**Needs:** the built-in browser on a linked PC (the `Claude_Browser` tools). No browser in the chat: say so in one line and stop there. Both sites played signed out; never sign in, and stop at a sign-in wall.

## Steps

1. **Open the post** with the tracking part of the link (everything from `?`) removed.
2. **Read the post's words first.** X: the page title and post text. Instagram: the `og:description` meta tag holds the whole caption. Often half the content is here.
3. **Start the video.** X: click the player once; its video has no picture until then. Instagram: it is ready on load. Then find the `video` element with `readyState > 0`, mute it, pause it, and note `duration`, `videoWidth`, `videoHeight`.
4. **Pick the sampling by what the video is:**
   - *Slides or on-screen text* (all text matters): run the change scan every 0.5 s. Capture the still 0.5 s before each change, plus one in the middle of any gap over 4 s. Text that types itself in is only complete at the end of its slide, so mid-slide stills show half sentences.
   - *Action* (a drill, a demo, a camera move): one still per second. The change scan is noise on handheld footage; skip it.
   - *Spoken words burned in one or two at a time*: also capture only the caption band, four times a second, as a grid of small strips. Near-complete narration in two screenshots.
5. **Draw contact sheets.** Seek, then draw each still into one full-window canvas with its time in the corner. Landscape video: 2 across, 3 down. Portrait: 4 across, 2 down. The canvas must be appended to `document.documentElement` with the top `z-index`, or the site's own layers cover it.
6. **Screenshot twice.** The pane draws late: the first screenshot after a sheet can be blank or half-filled. Take one throwaway at scale 0.1, then the real one.
7. **Clean up:** remove the canvas, leave the video paused.
8. **Report** what the video shows in your own words (never a full transcript of its text), and label the limits every time: no sound was heard; motion was sampled at the rate used; any text too small to read (try the zoom action on that region first).

## Code (run in the page)

```js
// setup, after the video is playing or ready
const v=[...document.querySelectorAll('video')].find(x=>x.readyState>0);
v.muted=true; v.pause(); window.__v=v;
window.__seek=t=>new Promise(res=>{let d=false;const f=()=>{if(!d){d=true;v.removeEventListener('seeked',f);setTimeout(res,120);}};
  v.addEventListener('seeked',f);v.currentTime=t;setTimeout(f,5000);});
const c=document.createElement('canvas');c.id='__cs';document.documentElement.appendChild(c);
c.width=innerWidth;c.height=innerHeight;
c.style.cssText='position:fixed;left:0;top:0;z-index:2147483647;background:#000;display:block';

// change scan: returns "time:score" pairs; a cut scores 20+, a text change 2-6 on a still background
window.__scan=async(a,b,step=0.5)=>{const s=document.createElement('canvas');s.width=96;s.height=54;
  const x=s.getContext('2d',{willReadFrequently:true});let p=null;const out=[];
  for(let t=a;t<b;t+=step){await window.__seek(t);x.drawImage(v,0,0,96,54);const d=x.getImageData(0,0,96,54).data;let n=0;
    if(p)for(let i=0;i<d.length;i+=4)n+=Math.abs(d[i]-p[i])+Math.abs(d[i+1]-p[i+1])+Math.abs(d[i+2]-p[i+2]);
    p=d;out.push(t+':'+(n/(96*54*3)).toFixed(1));}return out.join(' ');};

// contact sheet: times = list of seconds; cols x rows cells
window.__sheet=async(times,cols,rows)=>{const g=c.getContext('2d');g.fillStyle='#000';g.fillRect(0,0,c.width,c.height);
  const cw=c.width/cols,ch=c.height/rows,r=v.videoWidth/v.videoHeight;
  const w=Math.min(cw,ch*r),h=w/r;
  for(let i=0;i<times.length&&i<cols*rows;i++){await window.__seek(times[i]);
    const X=(i%cols)*cw+(cw-w)/2,Y=Math.floor(i/cols)*ch;g.drawImage(v,X,Y,w,h);
    g.fillStyle='rgba(0,0,0,.75)';g.fillRect(X,Y,50,16);g.fillStyle='#fff';g.font='12px sans-serif';g.fillText(times[i]+'s',X+4,Y+12);}
  return times;};

// caption strips: the band of the frame holding burned-in words (fractions of the frame), 4 per second
window.__strips=async(a,b,top=0.735,height=0.085)=>{const g=c.getContext('2d');g.fillStyle='#000';g.fillRect(0,0,c.width,c.height);
  const cols=6,rows=21,cw=c.width/cols,ch=c.height/rows;let i=0;
  for(let t=a;t<b&&i<cols*rows;t+=0.25,i++){await window.__seek(t);
    g.drawImage(v,v.videoWidth*0.08,v.videoHeight*top,v.videoWidth*0.84,v.videoHeight*height,Math.floor(i/rows)*cw+2,(i%rows)*ch+1,cw-4,ch-2);}
  return i;};   // reads down each column, then across

// cleanup
document.getElementById('__cs')?.remove(); window.__v.pause();
```

## What is and isn't proven

- Proven 2026-11-10: two X videos (2 min 14 s and 2 min 10 s) and one Instagram reel (56 s), all signed out, in the built-in browser on Charles's laptop.
- Not heard: audio. Speech with no burned-in words and no caption is lost. The fix would be downloading the file and transcribing it, which is not built (X is not on the allowed sites for the cloud workspace).
- Not tested: YouTube, other sites, posts behind a sign-in, Claude in Chrome, and any unattended run. Post Reader runs in the cloud with no PC browser, so it still reads only a video post's caption and preview.

Source: Charles, R&D chat 2026-11-10 ("search far and wide for a way for you to watch videos"); the blank-frame and half-sentence lessons come from that chat's own captures.
