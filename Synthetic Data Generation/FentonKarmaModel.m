% BCL in AU: basic cycle length: time between repeated stimuli (e.g.30)
% ncyc: number of cycles, number of times the cell is stimulated (e.g.10)
% extra in AU: time after BCL*ncyc during which the simulation runs (e.g.0)
% ncells is number of cells in 1D cable (e.g.200)
% iscyclic, = 0 for a cable, = 1 for a ring (connecting ends of the cable)
% flagmovie, = 1 to show movie of the potential propagating, = 0 otherwise

close all
clear all

savename='synthetic_data';
BCL=150;
ncyc=1;
extra=0;
ncells=100;
iscyclic=0;
flagmovie=1;

% one of the biggest determinants of the propagation speed
% (D should lead to realistic conduction velocities, i.e.
% between 0.6 and 0.9 m/s)
X = ncells + 2; % to allow boundary conditions implementation
stimgeo=false(X,1);
% comment or uncomment the two lines below to modify the stimulus side
stimgeo(1:5)=true; % indices of cells where external stimulus is felt (left)
%stimgeo(98:102)=true; % indices of cells where external stimulus is felt (right)

% Model parameters
dt=0.005; % AU, time step for finite differences solver
gathert=round(1/dt); % number of iterations at which V is outputted
% for plotting, set to correspond to 1 ms, regardless of dt
tend=BCL*ncyc+extra; % ms, duration of simulation
stimdur=1; % UA, duration of stimulus
Va=1.0; % AU, value for V when cell is stimulated
h = 0.1; % mm cell length
D = 0.1; % mm^2/ms, diffusion coefficient (for monodomain equation)

% initial data
ua=0.95;
v=0.99*ones(X,1); % v
w=0.99*ones(X,1); % w
u=zeros(X,1);

% parameters for Fenton-Karma model
uv=0.160; % uc for v
uw=0.160; % uc for w
uu=0.160; % uc for u
uvsi=0.040; % uv
ucsi=0.85; %uc_si r
k=10; % k
taud=0.125; % tau_d
tauv2=60; % tauv2-
tauv1=82.5; % tauv1-
tauvplus=5.75; % tauv+
tauo=32.5; % tauo
tauwminus=400; % tauw- 
tauwplus=300; % tauw+ 
taur=70; % taur
tausi=114; % tausi

usav=zeros(ncells,ceil(tend)); % array where U will be saved during simulation
Vsav=zeros(ncells,ceil(tend/gathert)); % array where V will be saved during simulation
Wsav=zeros(ncells,ceil(tend/gathert)); % array where W will be saved during simulation

ind=0; %iterations counter
kk=0; %counter for number of stimuli applied
t_array = 1:1:tend; % array holding time
x_array = 0.1:0.1:10; % array holding x positions

% for loop for explicit RK4 finite differences simulation
for t=dt:dt:tend % for every timestep
    ind=ind+1; % count interations
        % stimulate at every BCL time interval for ncyc times
        if t>=BCL*kk&&kk<ncyc
            u(stimgeo)=Va;

        end
        % stop stimulating after stimdur
        if t>=BCL*kk+stimdur
            kk=kk+1;
        end
        
        %fast inward current and gate
        Fu=zeros(X,1);
        vinf=ones(X,1);
        tauv=tauvplus.*ones(X,1);
        
        vinf(u>=uv)=0;
        tauv(u<uvsi&u<uv)=tauv1;
        tauv(u>=uvsi&u<uv)=tauv2;
        Fu(u>=uv)=(u(u>=uv)-uv).*(1-u(u>=uv));

        %fast inward current
        Jfi=Fu.*(-v)./taud;

        %update v
        v=v+(vinf-v)./tauv.*dt;

        %ungated outward current
        Uu=ones(X,1);
        Uu(u<=uu)=u(u<=uu);
        tauu=taur.*ones(X,1);
        tauu(u<=uu)=tauo;

        Jso=Uu./tauu;

        %slow inward current and slow gate
        winf=ones(X,1);
        winf(u>=uw)=0;
        tauw=tauwminus.*ones(X,1);
        tauw(u>=uw)=tauwplus;
        Jsi=-w./tausi.*0.5.*(1+tanh(k.*(u-ucsi)));

        % update w
        w=w+(winf-w)./tauw.*dt;

        % update u
        Iion=-(Jfi+Jsi+Jso);
        du=4*D.*del2(u,h);
        u=u+(Iion+du).*dt;
                      
        % rectangular boundary conditions: no flux of U
        if  ~iscyclic % 1D cable
            u(1)=u(2);
            u(end)=u(end-1);
        end
        
        % At every gathert iterations, save U value for plotting
        if mod(ind,gathert)==0
            % save values
            usav(:,round(ind/gathert))=u(2:end-1)';
            Wsav(:,round(ind/gathert))=w(2:end-1)';
            Vsav(:,round(ind/gathert))=v(2:end-1)';

            % show (thicker) cable
            if flagmovie
                imagesc(repmat(u(2:end-1)',[round(ncells/20) 1]),[0 1])
                axis image
                title([])
                set(gca,'FontSize',14)
                yticks(0)
                xlabel('x (voxels)')
                set(gca,'FontSize',14)
                title(['V (AU) - Time: ' num2str(t,'%.0f') ' ms'])
                colorbar
                pause(0.1)
            end
        end
end

w = w(2:end);
w(end) = [];
w = reshape(w,[1,100]);

usav = usav';
Vsav = Vsav';
Wsav = Wsav';

% Comment or Uncomment the three lines below depending on data wanted
save([savename '_usav_left_stim.mat'],'usav', 't_array', 'x_array', 'Wsav'); %left
%save([savename '_usav_right_stim.mat'],'usav', 't_array', 'x_array', 'Wsav'); %right
%save([savename '_UVWsav_extended.mat'],'usav', 't_array', 'x_array', 'Wsav', 'Vsav'); %right

% end

%% Plot usav
close all
figure()
[c,h] = contourf(usav');
set(gca,'fontsize',18)
set(gca,'TickLabelInterpreter','latex')
colormap('bone')
title('$u$ across Space and Time', 'FontSize', 20, 'Interpreter', 'latex')
xlabel('t (AU)', 'FontSize', 18, 'Interpreter', 'latex')
ylabel('x (AU)', 'FontSize', 18, 'Interpreter', 'latex')
colorbar

%% Plot Vsav
close all
figure()
plot(Vsav')
set(gca,'fontsize',18)
set(gca,'TickLabelInterpreter','latex')
title('Vsav', 'FontSize', 20, 'Interpreter', 'latex')
xlabel('t (AU)', 'FontSize', 18, 'Interpreter', 'latex')
ylabel('v (AU)', 'FontSize', 18, 'Interpreter', 'latex')

%% Plot Wsav
close all
figure()
plot(Wsav')
set(gca,'fontsize',18)
set(gca,'TickLabelInterpreter','latex')
title('Wsav', 'FontSize', 20, 'Interpreter', 'latex')
xlabel('t (AU)', 'FontSize', 18, 'Interpreter', 'latex')
ylabel('w (AU)', 'FontSize', 18, 'Interpreter', 'latex')
